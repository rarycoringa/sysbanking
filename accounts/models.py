from __future__ import annotations

import uuid
import decimal

from enum import Enum

from django.db import models
from django.core.validators import MinValueValidator

from accounts.exceptions import InsufficientBalance
from accounts.exceptions import NegativeTransaction

class AccountType(str, Enum):
    simple = "simple"
    bonus = "bonus"
    savings = "savings"


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
        validators=[MinValueValidator(decimal.Decimal(-1000.0))]
    )

    @property
    def type(self) -> str:     
        return AccountType.simple
    
    @property
    def verbose_type(self) -> str:
        return "Account"
    
    @property
    def minimum_balance_value(self) -> decimal.Decimal:
        return decimal.Decimal(-1000.0)

    def deposit(self, amount: decimal.Decimal) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        if amount < decimal.Decimal(0.0):
            raise NegativeTransaction("Unable to process transaction. Please enter a non-negative value for the transaction amount.")

        self.balance: decimal.Decimal = self.balance + amount

        self.save()

    def withdraw(self, amount: decimal.Decimal) -> None:
        if type(amount) is not decimal.Decimal:
            amount: decimal.Decimal = decimal.Decimal(amount)

        if amount < decimal.Decimal(0.0):
            raise NegativeTransaction("Unable to process transaction. Please enter a non-negative value for the transaction amount.")

        if (self.balance - amount) < self.minimum_balance_value:
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

        if amount < decimal.Decimal(0.0):
            raise NegativeTransaction("Unable to process transaction. Please enter a non-negative value for the transaction amount.")

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
        return AccountType.bonus

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

    def transfer_deposit(self, amount: decimal.Decimal, cutoff_amount: decimal.Decimal = decimal.Decimal(150.00)) -> None:
        self.deposit(amount, cutoff_amount)
    

class SavingsAccount(Account):
    @property
    def type(self) -> str:     
        return AccountType.savings

    @property
    def verbose_type(self) -> str:
        return "Savings Account"
    
    @property
    def minimum_balance_value(self) -> decimal.Decimal:
        return decimal.Decimal(0.0)

    @classmethod
    def generate_yield_for_savings_accounts(cls, taxes: decimal.Decimal) -> None:
        if type(taxes) is not decimal.Decimal:
            taxes:decimal.Decimal = decimal.Decimal(taxes)

        accounts = SavingsAccount.objects.all()

        for account in accounts:
            yields = (account.balance * taxes) / decimal.Decimal(100)
            account.deposit(yields)