from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import secrets
import uuid

# **CLOSELY TIED TO USER AUTHENTICATION FLOW MODELS**


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)

        if "salt" not in extra_fields:
            extra_fields["salt"] = secrets.token_hex(64)

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4
    )  # to prevent potential enumeration by attackers
    email = models.EmailField(unique=True)
    salt = models.CharField(
        max_length=128
    )  # for cryptographic operations ensures derivation of unique salt for users with the same credentials
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = None
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# for tracking authentication attempts
class PassKeyChallenge(models.Model):
    challenge = models.CharField(max_length=128, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="challenged")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    purpose = models.CharField(
        max_length=20,
        choices=[
            ("REGISTRATION", "Registration"),
            ("AUTHENTICATION", "Authentication"),
            ("TRANSACTION", "Transaction"),
        ],
    )
