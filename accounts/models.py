import uuid
import decimal

from django.db import models

class Account(models.Model):
    id: uuid.UUID = models.UUIDField(
        verbose_name="Identifier of Account",
        primary_key=True,
        unique=True,
        blank=False,
        null=False,
        default=uuid.uuid4,
        editable=False,
    )

    number: int = models.PositiveIntegerField(
        verbose_name="Number of Account",
        unique=True,
        blank=False,
        null=False,
    )

    balance: decimal.Decimal = models.DecimalField(
        verbose_name="Balance of Account",
        max_digits=15,
        decimal_places=2,
        blank=False,
        null=False,
        default=decimal.Decimal(0.0),
    )