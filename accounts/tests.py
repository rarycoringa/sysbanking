import decimal
import uuid

from django.test import TransactionTestCase
from django.db.utils import IntegrityError
from accounts.exceptions import NegativeTransaction

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
        self.assertEqual(account.type, AccountType.simple)

        self.assertNotIsInstance(account, BonusAccount)
        self.assertNotIsInstance(account, SavingsAccount)

    def test_retrieve_bonus_account_by_number(self):
        account = BonusAccount.objects.get(number=self.dummy_bonus_account.number)

        self.assertEqual(account, self.dummy_bonus_account)
        self.assertEqual(account.balance, self.dummy_bonus_account.balance)
        self.assertEqual(account.points, self.dummy_bonus_account.points)
        self.assertEqual(account.type, AccountType.bonus)

        self.assertIsInstance(account, Account)
        self.assertNotIsInstance(account, SavingsAccount)

    def test_retrieve_savings_account_by_number(self):
        account = SavingsAccount.objects.get(number=self.dummy_savings_account.number)

        self.assertEqual(account, self.dummy_savings_account)
        self.assertEqual(account.balance, self.dummy_savings_account.balance)
        self.assertEqual(account.type, AccountType.savings)

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
    def setUp(self):
        self.dummy_regular_account = Account.objects.create(number=100)
        self.dummy_bonus_account = BonusAccount.objects.create(number=200)
        self.dummy_savings_account = SavingsAccount.objects.create(number=300)

    def test_regular_deposit(self):
        self.assertEqual(self.dummy_regular_account.balance, 0)
        self.dummy_regular_account.deposit(100)
        self.assertEqual(self.dummy_regular_account.balance, 100)

    def test_negative_deposit(self):
        self.assertEqual(self.dummy_savings_account.balance, 0)
        with self.assertRaises(NegativeTransaction):
                self.dummy_savings_account.deposit(-100)

    def test_bonus_acc_benefits(self):
        test_list = [[0, 10, 100], 
                    [100, 11, 99],
                    [199, 11, 101],
                    [300, 12, 0]]
        for i in range (0, 4):
            self.assertEqual(self.dummy_bonus_account.balance, test_list[i][0])
            self.assertEqual(self.dummy_bonus_account.points, test_list[i][1])
            self.dummy_bonus_account.deposit(test_list[i][2])


class WithdrawTestCase(TransactionTestCase):
    ...


class TransferTestCase(TransactionTestCase):
    ...


class YieldsTestCase(TransactionTestCase):
    def setUp(self):
        self.number_balance_mapping = [
            (1, decimal.Decimal(100.0)),
            (2, decimal.Decimal(200.0)),
            (3, decimal.Decimal(300.0)),
        ]

    def test_generate_yields_for_savings_accounts(self):
        for number, initial_balance in self.number_balance_mapping:
            SavingsAccount.objects.create(number=number, balance=initial_balance)

        taxes = decimal.Decimal(50.0)

        SavingsAccount.generate_yield_for_savings_accounts(taxes=taxes)

        for number, initial_balance in self.number_balance_mapping:
            account = SavingsAccount.objects.get(number=number)
            
            self.assertNotEqual(account.balance, initial_balance)
            
            expected_balance = initial_balance + (initial_balance * taxes / decimal.Decimal(100.0))

            self.assertEqual(account.balance, expected_balance)

    def test_simple_account_should_not_generate_yields(self):
        for number, initial_balance in self.number_balance_mapping:
            Account.objects.create(number=number, balance=initial_balance)

        taxes = decimal.Decimal(50.0)

        SavingsAccount.generate_yield_for_savings_accounts(taxes=taxes)

        for number, initial_balance in self.number_balance_mapping:
            account = Account.objects.get(number=number)
            
            self.assertEqual(account.balance, initial_balance)

    def test_bonus_account_should_not_generate_yields(self):
        for number, initial_balance in self.number_balance_mapping:
            BonusAccount.objects.create(number=number, balance=initial_balance)

        taxes = decimal.Decimal(50.0)

        SavingsAccount.generate_yield_for_savings_accounts(taxes=taxes)

        for number, initial_balance in self.number_balance_mapping:
            account = Account.objects.get(number=number)
            
            self.assertEqual(account.balance, initial_balance)
    
    def test_simple_account_does_not_have_yields_feature(self):
        with self.assertRaises(AttributeError):
            Account.generate_yield_for_savings_accounts(taxes=10)

    def test_bonus_account_does_not_have_yields_feature(self):
        with self.assertRaises(AttributeError):
            BonusAccount.generate_yield_for_savings_accounts(taxes=10)