from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PassKeyCredential
from .serializers import (
    PassKeyRegistrationOptionsSerializer,
    PassKeyRegistrationVerifySerializer,
    PassKeyAuthenticationOptionsSerializer,
    PassKeyAuthenticationVerifySerializer,
    PassKeyCredentialSerializer,
)
from .services import PasskeyService, bytes_to_base64url, base64url_to_bytes
from utils.exception_handler import ErrorHandlingMixin
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["passkey"])
class PassKeyViewSet(ErrorHandlingMixin, viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    passkey_service = PasskeyService()

    @action(detail=False, methods=["get"])
    def generate_registration_options(self, request):
        """Generate WebAuthn registration options"""

        # use service to generate options
        options, challenge = self.passkey_service.generate_registration_options(
            request.user
        )

        # store challenge in session
        request.session["passkey_challenge"] = bytes_to_base64url(challenge)

        serializer = PassKeyRegistrationOptionsSerializer(options)
        # ? CAN is_valid BE CALLED
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def verify_registration(self, request):
        """Verify WebAuthn registration response"""
        # validate input data

        serializer = PassKeyRegistrationVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        challenge = base64url_to_bytes(request.session.get("passkey_challenge"))

        if not challenge:
            return Response(
                {"error": "No challenge found is session"},
                status=status.HTTP_404_NOT_FOUND,
            )

        credential, passkey_data = self.passkey_service.verify_registration(
            request.user, serializer.validated_data, challenge
        )
        request.session.pop("passkey_challenge", None)

        return Response(
            {
                "verified": True,
                "passkey": {
                    "id": credential.id,
                    "type": credential.algorithm_type,
                    "publicKey": credential.public_key,  # ? snake case
                },
            }
        )

    @action(detail=False, methods=["get"])
    def generate_authentication_options(self, request):
        """Generate WebAuthn authentication options"""
        # use sertice to generate options
        options, challenge = self.passkey_service.generate_authentication_options(
            request.user
        )
        # store challenge in session
        request.session["passkey_challenge"] = bytes_to_base64url(challenge)

        serializer = PassKeyAuthenticationOptionsSerializer(options)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def verify_authentication(self, request):

        serializer = PassKeyAuthenticationVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        challenge = base64url_to_bytes(request.session.get("passkey_challenge"))
        if not challenge:
            return Response(
                {"error": "No challenge found in session"},
                status=status.HTTP_404_NOT_FOUND,
            )

        credential = self.passkey_service.verify_authentication(
            request.user, serializer.validated_data, challenge
        )

        request.session.pop("passkey_challenge", None)

        return Response(
            {
                "verified": True,
                "credentialId": credential.id,
                "signature": serializer.validated_data["response"]["signature"],
                "authenticatorData": serializer.validated_data["response"][
                    "authenticatorData"
                ],
            }
        )

    @action(detail=False, methods=["get"])
    def list_passkeys(self, request):
        """list user's passkeys"""
        credentials = PassKeyCredential.objects.filter(user=request.user)

        serializer = PassKeyCredentialSerializer(credentials, many=True)

        return Response(serializer.data)

    @action(detail=True, methods=["delete"])
    def delete_passkey(self, request, pk=None):
        """Delete a passkey"""
        credential = PassKeyCredential.objects.get(id=pk, user=request.user)
        credential.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
