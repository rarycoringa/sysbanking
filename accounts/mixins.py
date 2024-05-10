import datetime

from typing import Any
from typing import Dict

from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from accounts.models import Account
from accounts.models import BonusAccount
from accounts.models import SavingsAccount


class CurrentYearMixin():
    current_year: int = datetime.date.today().year

    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
    
        context["current_year"] = self.current_year

        return context
    

class GetAccountMultipleTypesMixin():
    kwargs: Dict[str, Any]
    slug_field: str
    slug_url_kwarg: str

    def get_object(self) -> Account | BonusAccount | SavingsAccount:
        
        account: QuerySet[BonusAccount] = BonusAccount.objects.filter(
            **{self.slug_field: self.kwargs.get(self.slug_url_kwarg)}
        )

        if account:
            return account.get()

        account: QuerySet[SavingsAccount] = SavingsAccount.objects.filter(
            **{self.slug_field: self.kwargs.get(self.slug_url_kwarg)}
        )

        if account:
            return account.get()
        
        account: QuerySet[Account] = Account.objects.filter(
            **{self.slug_field: self.kwargs.get(self.slug_url_kwarg)}
        )
        
        return account.get()
    
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


class TemplateTitleMixin():
    template_title: str
    
    def get_context_data(self, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
    
        context["template_title"] = self.template_title

        return context


class TransactionValidationMixin():
    request: HttpRequest
    render_to_response: callable
    get_context_data: callable
    get_success_url: callable

    def transaction_valid(self, message: str = "Transaction sucessfully completed.") -> HttpResponseRedirect:
        """If the form is valid, redirect to the supplied URL."""
        messages.success(self.request, message, extra_tags="success")

        return HttpResponseRedirect(self.get_success_url())

    def transaction_invalid(self, reason: str = "Failed trying to do transaction.") -> HttpResponse:
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, reason, extra_tags="danger")

        return self.render_to_response(self.get_context_data())