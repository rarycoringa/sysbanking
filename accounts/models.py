import uuid
import decimal

from django.db import models

class Account(models.Model):
    id = models.UUIDField(
        verbose_name="Account Identifier",
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        default=uuid.uuid4,
        editable=False,
    )

    number = models.PositiveIntegerField(
        verbose_name="Account Number",
        unique=True,
        blank=False,
        null=False,
    )

    balance = models.DecimalField(
        verbose_name="Account Balance",
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        default=decimal.Decimal(0.0),
    )