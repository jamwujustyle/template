from django.db import models


class Transaction(models.Model):
    tx_hash = models.CharField(max_length=66, primary_key=True)
    account = models.ForeignKey(
        "wallets.Account", on_delete=models.CASCADE, related_name="transactions"
    )
    nonce = models.BigIntegerField()
    initiator_signer = models.ForeignKey(
        "wallets.Signer", on_delete=models.SET_NULL, null=True
    )
    user_op_hash = models.CharField(max_length=42)
    to_address = models.CharField(max_length=42)
    value = models.DecimalField(max_digits=36, decimal_places=36, default=0)
    data = models.TextField(null=True)
    gas_limit = models.BigIntegerField()
    gas_used = models.BigIntegerField(null=True)
    gas_price = models.BigIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("CONFIRMED", "Confirmed"),
            ("FAILED", "Failed")("CANCELLED", "Cancelled"),
        ],
        default="PENDING",
    )
    block_number = models.BigIntegerField(null=True)
    chain_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True)
