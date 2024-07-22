from django.db.models.query import QuerySet

from accounts.models import Account
from accounts.models import BonusAccount
from accounts.models import SavingsAccount


class GetAccountMultipleTypesMixin():
    
    def get_account_by_number(self, number: int) -> Account | BonusAccount | SavingsAccount:
        account: QuerySet[BonusAccount] = BonusAccount.objects.filter(
            number=number,
        )

        if account:
            return account.get()

        account: QuerySet[SavingsAccount] = SavingsAccount.objects.filter(
            number=number,
        )

        if account:
            return account.get()
        
        account: QuerySet[Account] = Account.objects.filter(
            number=number,
        )
        
        return account.get()