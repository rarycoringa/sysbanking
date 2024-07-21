from typing import Dict
from typing import List
from typing import Set

from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from accounts.models import AccountType
from accounts.models import Account
from accounts.models import BonusAccount
from accounts.models import SavingsAccount
from restapi.mixins import GetAccountMultipleTypesMixin
from restapi.serializers import AccountSerializer
from restapi.serializers import BonusAccountSerializer
from restapi.serializers import SavingsAccountSerializer
from restapi.serializers import DetailAccountSerializer
from restapi.serializers import DetailBonusAccountSerializer
from restapi.serializers import DetailSavingsAccountSerializer
from restapi.serializers import TransactionSerializer
from restapi.serializers import GenerateYieldsSerializer


class AccountListAPIView(APIView):
    serializer_class_map: Dict[str, AccountSerializer] = {
        AccountType.simple.value: AccountSerializer,
        AccountType.bonus.value: BonusAccountSerializer,
        AccountType.savings.value: SavingsAccountSerializer,
    }

    def get(self, request: Request, format=None) -> Response:
        accounts: Set[Account] = self.get_all_accounts()
        serializer: ModelSerializer = AccountSerializer(accounts, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request, format=None) -> Response:
        account_type: str = request.data.get("type", AccountType.simple.value)
        serializer_cls: AccountSerializer = self.serializer_class_map[account_type]
        
        request.data.pop("type")

        serializer: ModelSerializer = serializer_cls(data=request.data)

        serializer.is_valid(raise_exception=True)
        account: Account = serializer.create()

        serializer: AccountSerializer = serializer_cls(account)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get_all_accounts(self) -> Set[Account | BonusAccount | SavingsAccount]:
        simple_accounts: List[Account] = [
            account for account in Account.objects.filter(
                bonusaccount__isnull=True,
                savingsaccount__isnull=True,
            )
        ]

        bonus_accounts: List[BonusAccount] = [
            account for account in BonusAccount.objects.all()
        ]

        savings_accounts: List[SavingsAccount] = [
            account for account in SavingsAccount.objects.all()
        ]

        all_accounts: Set[Account | BonusAccount | SavingsAccount] = {
            account for account in simple_accounts + bonus_accounts + savings_accounts
        }

        return all_accounts


class AccountDetailAPIView(APIView, GetAccountMultipleTypesMixin):
    serializer_class_map: Dict[str, AccountSerializer] = {
        AccountType.simple.value: DetailAccountSerializer,
        AccountType.bonus.value: DetailBonusAccountSerializer,
        AccountType.savings.value: DetailSavingsAccountSerializer,
    }

    def get(self, request: Request, number: int, format=None) -> Response:
        try:
            account: Account = self.get_account_by_number(number)
        except:
            return Response("Account not found", status.HTTP_404_NOT_FOUND)

        serializer_cls: AccountSerializer = self.serializer_class_map[account.type]

        serializer: ModelSerializer = serializer_cls(account)

        return Response(serializer.data, status.HTTP_200_OK)


class AccountDepositAPIView(APIView, GetAccountMultipleTypesMixin):
    
    def put(self, request: Request, number: int, format=None) -> Response:
        try:
            account: Account = self.get_account_by_number(number)
        except:
            return Response("Account not found", status.HTTP_404_NOT_FOUND)

        serializer: TransactionSerializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account.deposit(amount=serializer.validated_data["amount"])

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class AccountTransferAPIView(APIView):
    
    def put(self, request: Request, number, format=None):
        ...


class AccountWithdrawAPIView(APIView, GetAccountMultipleTypesMixin):
    
    def put(self, request: Request, number: int, format=None) -> Response:
        try:
            account: Account = self.get_account_by_number(number)
        except:
            return Response("Account not found", status.HTTP_404_NOT_FOUND)

        serializer: TransactionSerializer = TransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account.withdraw(amount=serializer.validated_data["amount"])

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class GenerateYieldAPIView(APIView):

    def put(self, request: Request, format=None):
        serializer: GenerateYieldsSerializer = GenerateYieldsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        SavingsAccount.generate_yield_for_savings_accounts(serializer.validated_data["tax"])

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)