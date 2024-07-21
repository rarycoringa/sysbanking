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
    def setUp(self):
        self.dummy_simple_account = Account.objects.create(number=997, balance=100.0)
        self.dummy_bonus_account = BonusAccount.objects.create(number=998, balance=200.0, points=15)
        self.dummy_savings_account = SavingsAccount.objects.create(number=999, balance=300.0)

        self.dummy_accounts = [
            self.dummy_simple_account,
            self.dummy_bonus_account.account_ptr,
            self.dummy_savings_account.account_ptr,
        ]

    def test_retrieve_all_accounts(self):
        accounts = Account.objects.all()

        self.assertEqual(len(accounts), len(self.dummy_accounts))
        self.assertCountEqual(accounts, self.dummy_accounts)

    def test_retrieve_simple_account_by_number(self):
        account = Account.objects.get(number=self.dummy_simple_account.number)

        self.assertEqual(account, self.dummy_simple_account)
        self.assertEqual(account.balance, self.dummy_simple_account.balance)
        
        self.assertNotIsInstance(account, BonusAccount)
        self.assertNotIsInstance(account, SavingsAccount)

    def test_retrieve_bonus_account_by_number(self):
        account = BonusAccount.objects.get(number=self.dummy_bonus_account.number)

        self.assertEqual(account, self.dummy_bonus_account)
        self.assertEqual(account.balance, self.dummy_bonus_account.balance)
        self.assertEqual(account.points, self.dummy_bonus_account.points)

        self.assertIsInstance(account, Account)
        self.assertNotIsInstance(account, SavingsAccount)

    def test_retrieve_savings_account_by_number(self):
        account = SavingsAccount.objects.get(number=self.dummy_savings_account.number)

        self.assertEqual(account, self.dummy_savings_account)
        self.assertEqual(account.balance, self.dummy_savings_account.balance)

        self.assertIsInstance(account, Account)
        self.assertNotIsInstance(account, BonusAccount)

    def test_simple_account_does_not_exists(self):
        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(number=0)

    def test_bonus_account_does_not_exists(self):
        with self.assertRaises(BonusAccount.DoesNotExist):
            BonusAccount.objects.get(number=0)

    def test_savings_account_does_not_exists(self):
        with self.assertRaises(SavingsAccount.DoesNotExist):
            SavingsAccount.objects.get(number=0)


class DepositTestCase(TransactionTestCase):
    ...


class WithdrawTestCase(TransactionTestCase):
    ...


class TransferTestCase(TransactionTestCase):
    ...


class YieldsTestCase(TransactionTestCase):
    ...