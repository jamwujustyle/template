from django.db import models
import uuid


class Factory(models.Model):
    factory_address = models.CharField(max_length=42, unique=True, primary_key=True)
    implementation_address = models.CharField(max_length=42)
    chain_id = models.IntegerField()
    first_seen_block = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Account(models.Model):
    account_address = models.CharField(max_length=42, primary_key=True)
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="accounts"
    )
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    # creator_address = models.CharField(max_length=42) QUESTIONABLE (CREATOR ADDRESS MIGHT NOT EXIST ACCOUNT COULD BE DEPLOYED BY FACTORY)
    creator_salt = models.CharField(max_length=128, null=True)
    creation_block = models.BigIntegerField()
    creation_tx_hash = models.CharField(max_length=66)
    chain_id = models.IntegerField()
    version = models.CharField(max_length=16)
    # balance_eth = models.DecimalField(max_digits=36, decimal_places=18, default=0) QUESTIONABLE NEEDS ADJUSTMENTS
    nonce = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Signer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="signers"
    )
    passkey_credential = models.ForeignKey(
        "passkeys.PassKeyCredential",
        on_delete=models.SET_NULL,
        null=True,
        related_name="signers",
    )
    signer_type = models.CharField(
        max_length=10, choices=[("ECDSA", "ECDSA"), ("RSA", "RSA"), ("P256", "P256")]
    )
    public_key_data = models.TextField()
    is_active = models.BooleanField(default=True)
    added_block = models.BooleanField()
    added_tx_hash = models.CharField(max_length=66)
    removed_block = models.BigIntegerField(null=True)
    removed_tx_hash = models.CharField(max_length=66, null=True)
    chain_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    weight = models.IntegerField(default=1)  # for mulisig threshold
