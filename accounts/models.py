import uuid
import decimal

from django.db import models
from django.core.validators import MinValueValidator

from accounts.exceptions import InsufficientBalance


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
        validators=[MinValueValidator(decimal.Decimal(0.0))]
    )

    def deposit(self, amount: decimal.Decimal) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        self.balance: decimal.Decimal = self.balance + amount

        self.save()
    
    def transfer(self, amount: decimal.Decimal, to_account: int) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        if self.balance < amount:
            raise InsufficientBalance("Account doesn't have sufficient balance.")

        if type(amount) is not int:
            to_account: int = int(to_account)

        to_account: Account = Account.objects.get(number=to_account)

        self.withdraw(amount)
        to_account.deposit(amount)
        
        self.save()
        to_account.save()
        
    def withdraw(self, amount: decimal.Decimal) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        if self.balance < amount:
            raise InsufficientBalance("Account doesn't have sufficient balance.")

        self.balance = self.balance - amount

        self.save()
