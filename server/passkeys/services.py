from fido2.webauthn import (
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    AttestationConveyancePreference,
)
from fido2.webauthn import PublicKeyCredentialRpEntity, PublicKeyCredentialUserEntity
from fido2.server import Fido2Server
import base64
import binascii
from core.models import User
from fido2 import cbor
from django.conf import settings
from django.utils import timezone
from .models import PassKeyCredential

# from fido2.utils import base64url_to_bytes, bytes_to_base64url


def base64url_to_bytes(base64url_string: str):
    """convert a base64url string to bytes"""
    if not base64url_string:
        return b""
    base64_string = base64url_string.replace("-", "+").replace("_", "/")

    padded = base64_string + "=" * (4 - len(base64_string) % 4) % 4

    try:
        return base64.b64decode(padded)
    except binascii.Error:
        raise ValueError(f"Invalid base64url string: {base64url_string}")


def bytes_to_base64url(bytes_data: bytes):
    """convert bytes to a base64url string"""
    if not bytes_data:
        return ""
    base64_string = base64.b64encode(bytes_data).decode("ascii")

    return base64_string.replace("+", "-").replace("/", "_").rstrip("=")


class PasskeyService:
    """
    Service for handling passkey operations
    """

    def __init__(self):
        self.rp = PublicKeyCredentialRpEntity(settings.RP_NAME, settings.RP_ID)
        self.server = Fido2Server(self.rp)

    def generate_registration_options(self, user: "User"):
        """generate options for registering a new passkey"""
        user_entity = PublicKeyCredentialUserEntity(
            id=str(user.id).encode("utf-8"),
            name=user.email,
            display_name=user.get_full_name() or user.email,
        )
        # get existing cred for this user
        existing_credentials = [
            bytes(cred.id, "utf-8")
            for cred in PassKeyCredential.objects.filter(user=user)
        ]

        # generate registration options
        options = self.server.register_begin(
            user_entity,
            existing_credentials,
            user_verification=UserVerificationRequirement.PREFERRED,
            authenticator_selector=AuthenticatorSelectionCriteria(
                resident_key="preferred", user_verification="preferred"
            ),
            attestation=AttestationConveyancePreference.NONE,
        )

        # format the response for the client
        registration_options = {
            "challenge": bytes_to_base64url(options.challenge),
            "rp": {
                "name": options.rp.name,
                "id": options.rp.id,
            },
            "user": {
                "id": bytes_to_base64url(options.user.id),
                "name": options.user.name,
                "displayName": options.user.display_name,
            },
            "pubKeyCredParams": [
                {"type": "public-key", "alg": alg} for alg in [-7, -257]  # ES256, RS256
            ],
            "timeout": 60000,
            "attestation": "none",
            "authenticatorSelection": {
                "residentKey": "preferred",
                "userVerification": "preferred",
            },
        }
        return registration_options, options.challenge

    def verify_registration(self, user, attestation_response, challenge):
        """
        verify the registration response and create credential
        """
        formatted_response = {
            "id": attestation_response["id"],
            "rawId": base64url_to_bytes(attestation_response["rawId"]),
            "response": {
                "clientDataJSON": base64url_to_bytes(
                    attestation_response["response"]["clientDataJSON"]
                ),
                "attestationObject": base64url_to_bytes(
                    attestation_response["response"]["attestationObject"]
                ),
            },
            "type": attestation_response["type"],
        }

        # verify attestation
        auth_data = self.server.register_complete(
            challenge,
            formatted_response,
        )

        # determine passkey type
        passkey_type, passkey_data = self._determine_passkey_type(
            auth_data.credential_data
        )

        # save the credential
        credential = PassKeyCredential.objects.create(
            id=attestation_response["id"],
            user=user,
            public_key=bytes_to_base64url(auth_data.credential_data.public_key),
            algorithm_type=passkey_type,
            attestation_object=bytes_to_base64url(
                attestation_response["response"]["attestationObject"]
            ),
            signature_counter=auth_data.counter,
        )

        return credential, passkey_data

    def generate_authentication_options(self, user):
        """generate options for authenticating with a passkey"""

        credentials = list(PassKeyCredential.objects.filter(user=user))

        if not credentials:
            raise ValueError("No credentials found for this user")

        options = self.server.authenticate_begin(
            [bytes_to_base64url(cred.id) for cred in credentials],
            user_verification=UserVerificationRequirement.PREFERRED,
        )

        authentication_options = {
            "challenge": bytes_to_base64url(options.challenge),
            "rpId": settings.RP_ID,
            "allowCredentials": [
                {
                    "id": cred.id,
                    "type": "public-key",
                    "transports": list(
                        cred.transports
                        if hasattr(cred, "transports") and cred.transports
                        else []
                    ),
                }
                for cred in credentials
            ],
            "timeout": 60000,
            "userVerification": "preferred",
        }

        return authentication_options, options.challenge

    def verify_authentication(self, user, assertion_response, challenge):
        """verify the authentication response"""
        try:
            credential = PassKeyCredential.objects.get(
                id=assertion_response["id"], user=user
            )
        except PassKeyCredential.DoesNotExist:
            raise ValueError("Credential not found")

        formatted_response = {
            "id": assertion_response["id"],
            "rawId": base64url_to_bytes(assertion_response["rawId"]),
            "response": {
                "clientDataJSON": base64url_to_bytes(
                    assertion_response["response"]["clientDataJSON"]
                ),
                "authenticatorData": base64url_to_bytes(
                    assertion_response["response"]["authenticatorData"]
                ),
                "signature": base64url_to_bytes(
                    assertion_response["response"]["signature"]
                ),
                "userHandle": (
                    base64url_to_bytes(
                        assertion_response["response"].get("userHandle", "")
                    )
                    if assertion_response["response"].get("userHandle")
                    else None
                ),
            },
            "type": assertion_response["type"],
        }
        auth_data = self.server.authenticate_complete(
            challenge, credential, formatted_response
        )

        credential.signature_counter = auth_data.counter
        credential.last_used = timezone.now()
        credential.save()

        return credential

    def _determine_passkey_type(self, credential_data):
        """determine the type of passkey from credential data"""
        public_key = credential_data.public_key
        cose_key = cbor.decode(public_key)

        # get the key type (kty)
        kty = cose_key.get(1)  # 1 is kty is COSE

        if kty == 2:  # EC2 key (p-256)
            # get the x and y coordinated
            x = cose_key.get(-2)  # -2 x
            y = cose_key.get(-3)  # -3 y

            if not x or not y:
                raise ValueError("EC2 key missing x or y coordinates")

            qx = "0x" + x.hex()
            qy = "ox" + y.hex()

            return "P256", {"qx": qx, "qy": qy}

        elif kty == 3:  # RSA key
            # get the modulus and exponent
            n = cose_key.get(-1)  # -1 is n in COSE
            e = cose_key.get(-2)  # -2 is e in COSE

            if not n or not e:
                raise ValueError("RSA key missing n or e parameters")

            n_hex = "0x" + n.hex()
            e_hex = "0x" + e.hex()

            return "RSA", {"n": n_hex, "e": e_hex}
        else:
            # default to ecdsa for other key types
            return "ECDSA", {"publicKey": bytes_to_base64url(public_key)}
