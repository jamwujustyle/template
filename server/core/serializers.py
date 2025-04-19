from django.contrib.auth import authenticate
from rest_framework import serializers
from logging_config import logger
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"required": True},
            "salt": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def validate_salt(self, salt):
        if len(salt) != 128:
            raise serializers.ValidationError("Salt must be 128 characters long")
        return salt

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        keys = ["created_at", "salt"]
        _ = [repr.pop(key) for key in keys]

        return repr

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None

        if user and user.is_authenticated:
            instance, _ = User.objects.get_or_create(
                email=user.email, defaults=validated_data
            )
            return instance

        # Use the custom manager's create_user method to ensure password hashing
        password = validated_data.pop("password", None)
        user = User.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True
    )  # Add write_only=True for security

    def validate(self, data):
        # Correctly pass the actual password from the input data
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data["user"] = user
        return data
