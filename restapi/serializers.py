from rest_framework import serializers

from accounts.models import Account
from accounts.models import BonusAccount
from accounts.models import SavingsAccount


class AccountSerializer(serializers.ModelSerializer):
    
    def create(self) -> Account | BonusAccount | SavingsAccount:
        return self.Meta.model.objects.create(**self.validated_data)

    class Meta:
        model = Account
        fields = ['id', 'number', 'type']


class BonusAccountSerializer(AccountSerializer):

    class Meta:
        model = BonusAccount
        fields = ['id', 'number', 'type']


class SavingsAccountSerializer(AccountSerializer):

    class Meta:
        model = SavingsAccount
        fields = ['id', 'number', 'type']


class DetailAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'number', 'balance', 'type']


class DetailBonusAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BonusAccount
        fields = ['id', 'number', 'balance', 'points', 'type']


class DetailSavingsAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingsAccount
        fields = ['id', 'number', 'balance', 'type']


class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=15, decimal_places=2)


class GenerateYieldsSerializer(serializers.Serializer):
    tax = serializers.DecimalField(max_digits=15, decimal_places=2)
