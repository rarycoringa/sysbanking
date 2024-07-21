import decimal
import uuid

from django.test import TransactionTestCase
from django.db.utils import IntegrityError

from accounts.models import AccountType
from accounts.models import Account
from accounts.models import BonusAccount
from accounts.models import SavingsAccount


class CreateAccountTestCase(TransactionTestCase):
    def setUp(self):
        self.dummy_accounts = [995, 996, 997, 998, 999]

    def test_create_simple_account(self):
        for number in self.dummy_accounts:
            Account.objects.create(number=number)
            
            account = Account.objects.get(number=number)

            self.assertIsInstance(account.id, uuid.UUID)
            self.assertEqual(account.number, number)
            self.assertEqual(account.balance, decimal.Decimal(0.0))
            self.assertEqual(account.type, AccountType.simple)

    def test_create_bonus_account(self):
        for number in self.dummy_accounts:
            BonusAccount.objects.create(number=number)
            
            account = BonusAccount.objects.get(number=number)

            self.assertIsInstance(account.id, uuid.UUID)
            self.assertEqual(account.number, number)
            self.assertEqual(account.balance, decimal.Decimal(0.0))
            self.assertEqual(account.type, AccountType.bonus)
            self.assertEqual(account.points, 10)

    def test_create_savings_account(self):
        for number in self.dummy_accounts:
            SavingsAccount.objects.create(number=number)
            
            account = SavingsAccount.objects.get(number=number)

            self.assertIsInstance(account.id, uuid.UUID)
            self.assertEqual(account.number, number)
            self.assertEqual(account.balance, decimal.Decimal(0.0))
            self.assertEqual(account.type, AccountType.savings)

    def test_create_account_with_number_already_in_use(self):
        for number in self.dummy_accounts:
            Account.objects.create(number=number)

        for number in self.dummy_accounts:
            with self.assertRaises(IntegrityError):
                Account.objects.create(number=number)


class RetrieveAccountTestCase(TransactionTestCase):
    ...


class RetrieveAccountBalanceTestCase(TransactionTestCase):
    ...


class DepositTestCase(TransactionTestCase):
    ...


class WithdrawTestCase(TransactionTestCase):
    ...


class TransferTestCase(TransactionTestCase):
    ...


class YieldsTestCase(TransactionTestCase):
    ...