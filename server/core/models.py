import uuid
from django.db import models

# **CLOSELY TIED TO USER AUTHENTICATION FLOW MODELS**


class UserManager(models.Manager):
    def create_user(self, email):
        salt = self._generate_salt()
        return self.create(email=email, salt=salt)

    def _generate_salt(self):
        return uuid.uuid4().hex


class User(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4
    )  # to prevent potential enumeration by attackers
    email = models.EmailField(unique=True)
    salt = models.CharField(
        max_length=128
    )  # for cryptographic operations ensures derivation of unique salt for users with the same credentials
    created_at = models.DateTimeField(auto_now_add=True)


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
