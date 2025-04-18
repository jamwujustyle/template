from django.db import models


class PassKeyCredential(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="credentials"
    )
    public_key = models.TextField()  # store in PEM or DER format
    algorithm_type = models.CharField(
        max_length=10, choices=[("ECDSA", "ECDSA"), ("RSA", "RSA"), ("P256", "P256")]
    )
    attestation_object = models.TextField(null=True)
    signature_counter = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True)
