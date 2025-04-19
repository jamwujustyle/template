from rest_framework import serializers
from .models import PassKeyCredential
from django.core.exceptions import ValidationError


class PassKeyOptionsSerializer(serializers.Serializer):
    """Base serializer for passkey options

    Args:
        serializers (_type_): _description_
    """

    challenge = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError("This serializer is not meant for creating objects")

    def update(self, instance, validated_data):
        raise NotImplemented("This serializer is not meant for updating objects")


class PassKeyRegistrationOptionsSerializer(PassKeyOptionsSerializer):
    """Serializer for generating registration options

    Args:
        PassKeyOptionsSerializer (_type_): _description_
    """

    rp = serializers.DictField(read_only=True)
    user = serializers.DictField(read_only=True)
    pubKeyCredParams = serializers.ListField(read_only=True)
    timeout = serializers.IntegerField(read_only=True)
    attestation = serializers.CharField(read_only=True)
    authenticatorSelection = serializers.DictField(read_only=True)

    def to_representation(self, instance):
        return instance


class PassKeyRegistrationVerifySerializer(serializers.Serializer):
    """Serializer for verifying registration response

    Args:
        serializers (_type_): _description_
    """

    id = serializers.CharField()
    rawId = serializers.CharField()
    type = serializers.CharField()
    clientExtensionResults = serializers.DictField(required=False, default=dict)

    # nested response serializer
    response = serializers.DictField()

    def validate_response(self, response):
        """validate the response data"""
        required_fields = ["clientDataJSON", "attestationObject"]

        missing = [field for field in required_fields if field not in response]

        if missing:
            raise serializers.ValidationError(
                f"Missing required field(s): {','.join(missing) }"
            )

    def validate(self, data):
        """validate the entire data"""
        if data["type"] != "public-key":
            raise serializers.ValidationError("Type must be 'public-key'")
        return data

    def create(self, validated_data):
        raise NotImplementedError("This serializer is not meant for creating objects")

    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer is not meant for updating objects")


class PassKeyAuthenticationOptionsSerializer(PassKeyOptionsSerializer):
    """Serializer for generating authentication options

    Args:
        PassKeyOptionsSerializer (_type_): _description_
    """

    rpId = serializers.CharField(read_only=True)
    allowCredentials = serializers.ListField(read_only=True)
    timeout = serializers.IntegerField(read_only=True)
    userVerification = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        return instance


class PassKeyAuthenticationVerifySerializer(serializers.Serializer):
    """Serializer for verifying authentication response

    Args:
        serializers (_type_): _description_
    """

    id = serializers.CharField()
    rawId = serializers.CharField()
    type = serializers.CharField()
    clientExtensionResults = serializers.DictField(required=False, default=dict)

    # nested response serializer
    response = serializers.DictField()

    def validate_response(self, response):
        """validate the response data"""
        required_fields = ["clientDataJSON", "authenticatorData", "signature"]

        missing = [field for field in required_fields if field not in response]
        if missing:
            raise serializers.ValidationError(
                f"Missing required fields: { (',').join(missing)}"
            )

    def validate(self, data):
        """validate the entire data"""
        if data["type"] != "public-key":
            raise serializers.ValidationError("Type must be 'public-key'")
        return data

    def create(self, validated_data):
        raise NotImplementedError("This serializer is not meant for creating objects")

    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer is not meant for updating objects")


class PassKeyCredentialSerializer(serializers.ModelSerializer):
    """Serializer for the PassKeyCredential model"""

    class Meta:
        model = PassKeyCredential
        # ? ALL OR EXCLUDE ATTESTATION_OBJECT ?
        fields = "__all__"
        read_only_fields = ["id", "created_at", "last_used"]
