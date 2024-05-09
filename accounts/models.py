from __future__ import annotations

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

    @property
    def type(self) -> str:     
        return "simple"
    
    @property
    def verbose_type(self) -> str:
        return "Account"

    def deposit(self, amount: decimal.Decimal) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        self.balance: decimal.Decimal = self.balance + amount

        self.save()

    def withdraw(self, amount: decimal.Decimal) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        if self.balance < amount:
            raise InsufficientBalance("Account doesn't have sufficient balance.")

        self.balance: decimal.Decimal = self.balance - amount

        self.save()
    
    def transfer_deposit(self, amount: decimal.Decimal) -> None:
        self.deposit(amount)

    def transfer_withdraw(self, amount: decimal.Decimal) -> None:
        self.withdraw(amount)

    @staticmethod
    def transfer(amount: decimal.Decimal, from_account: Account, to_account: Account) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        from_account.transfer_withdraw(amount)
        to_account.transfer_deposit(amount)


class BonusAccount(Account):
    points = models.PositiveIntegerField(
        verbose_name="Account Points",
        blank=False,
        null=False,
        default=10,
    )

    @property
    def type(self) -> str:     
        return "bonus"

    @property
    def verbose_type(self) -> str:
        return "Bonus Account"
    
    def add_points(self, amount: decimal.Decimal, cutoff_amount: decimal.Decimal) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        if type(cutoff_amount) is not decimal.Decimal:
            cutoff_amount: decimal.Decimal = decimal.Decimal(cutoff_amount)

        points: int = int(amount // cutoff_amount)

        self.points: decimal.Decimal = self.points + points
        
        self.save()

    def deposit(self, amount: decimal.Decimal, cutoff_amount: decimal.Decimal = decimal.Decimal(100.00)) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        self.balance: decimal.Decimal = self.balance + amount

        self.add_points(amount, cutoff_amount)

        self.save()

    def transfer_deposit(self, amount: decimal.Decimal, cutoff_amount: decimal.Decimal = decimal.Decimal(200.00)) -> None:
        self.deposit(amount, cutoff_amount)
    