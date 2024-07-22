from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import Union
from typing import Callable

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models.base import Model
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from accounts.mixins import CurrentYearMixin
from accounts.mixins import GetAccountMultipleTypesMixin
from accounts.mixins import TemplateTitleMixin
from accounts.mixins import TransactionValidationMixin
from accounts.models import Account
from accounts.models import BonusAccount
from accounts.models import SavingsAccount


class ListAccountView(CurrentYearMixin, TemplateTitleMixin, ListView):
    context_object_name: str = "accounts"
    model: Account = Account
    template_name: str = "accounts/list.html"
    template_title: str = "Account List"

    def get_queryset(self) -> Set[Account | BonusAccount | SavingsAccount]:
        simple_accounts: List[Account] = [
            account for account in self.model.objects.filter(
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


class DetailAccountView(CurrentYearMixin, GetAccountMultipleTypesMixin, TemplateTitleMixin, DetailView):
    context_object_name: str = "account"
    model: Account = Account
    slug_field: str = "number"
    slug_url_kwarg: str = "number"
    template_name: str = "accounts/detail.html"
    template_title: str = "Account Details"

    def get_context_data(self: View, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        context_data: Dict[str, Any] = super().get_context_data(**kwargs)

        retrieved_messages: List[Any] = messages.get_messages(self.request)

        if retrieved_messages:
            context_data["messages"] = retrieved_messages

        return context_data
    

class CreateAccountView(SuccessMessageMixin, CurrentYearMixin, TemplateTitleMixin, CreateView):
    fields: List[str] = ["number", "balance"]
    model: Account = Account
    success_url = reverse_lazy('accounts:create')
    template_name: str = "accounts/create.html"
    template_title: str = "Create Accounts"
    model_class_map: Dict[str, Account] = {
        "simple": Account,
        "bonus": BonusAccount,
        "savings": SavingsAccount,
    }

    def get_success_message(self, cleaned_data: Dict[str, str]) -> str:
        account: Account = self.object
        return f"Account Nº {account.number} was successfully created."
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        type: str = request.POST.get("type")

        self.model: Account | BonusAccount | SavingsAccount = self.model_class_map[type]

        return super().post(request, *args, **kwargs)


class TransactionView(GetAccountMultipleTypesMixin, TransactionValidationMixin, DetailView):
    transaction_name: str
    transaction_parameters_names: List[str]

    def post(self, request: HttpRequest, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        self.object: Account | BonusAccount = self.get_object()

        transaction_parameters: Dict[str, Any] = {
            param: request.POST[param]
            for param in self.transaction_parameters_names
        }
        
        transaction_method: Callable = self.object.__getattribute__(self.transaction_name)

        try:
            transaction_method(**transaction_parameters)
        except ValidationError as err:
            return self.transaction_invalid(err.message)

        success_message: str = f"{self.transaction_name.title()} successfuly completed."

        return self.transaction_valid(success_message)


class MakeDepositView(TemplateTitleMixin, CurrentYearMixin, TransactionView):
    context_object_name: str = "account"
    model: Account = Account
    slug_field: str = "number"
    slug_url_kwarg: str = "number"
    template_name: str = "accounts/deposit.html"
    template_title: str = "Make Deposit"
    transaction_name: str  = "deposit"
    transaction_parameters_names: List[str] = ["amount"]

    def get_success_url(self) -> str:
        return reverse_lazy('accounts:detail', kwargs={"number": self.object.number})


class MakeWithdrawView(TemplateTitleMixin, CurrentYearMixin, TransactionView):
    context_object_name: str = "account"
    model: Account = Account
    slug_field: str = "number"
    slug_url_kwarg: str = "number"
    template_name: str = "accounts/withdraw.html"
    template_title: str = "Make Withdraw"
    transaction_name: str  = "withdraw"
    transaction_parameters_names: List[str] = ["amount"]

    def get_success_url(self) -> str:
        return reverse_lazy('accounts:detail', kwargs={"number": self.object.number})
    

class TransferView(GetAccountMultipleTypesMixin, TransactionValidationMixin, DetailView):
    transaction_name: str
    transaction_parameters_names: List[str]
    model: Account

    def post(self, request: HttpRequest, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        self.object: Account | BonusAccount = self.get_object()

        transaction_parameters: Dict[str, Any] = {
            param: request.POST[param]
            for param in self.transaction_parameters_names
        }
        
        from_account: Account | BonusAccount = self.object
        transaction_parameters["from_account"] = from_account

        to_account: Account | BonusAccount = self.get_account_by_number(
            transaction_parameters["to_account"],
        )
        transaction_parameters["to_account"] = to_account

        transaction_method: Callable = self.model.transfer

        try:
            transaction_method(**transaction_parameters)
        except ValidationError as err:
            return self.transaction_invalid(err.message)

        success_message: str = f"{self.transaction_name.title()} successfuly completed."

        return self.transaction_valid(success_message)


class MakeTransferView(TemplateTitleMixin, CurrentYearMixin, TransferView):
    context_object_name: str = "account"
    model: Account = Account
    slug_field: str = "number"
    slug_url_kwarg: str = "number"
    template_name: str = "accounts/transfer.html"
    template_title: str = "Transfer"
    transaction_name: str  = "transfer"
    transaction_parameters_names: List[str] = ["amount", "to_account"]

    def get_success_url(self) -> str:
        return reverse_lazy('accounts:detail', kwargs={"number": self.object.number})


class GenerateYieldsView(TemplateTitleMixin, CurrentYearMixin, TemplateView):
    template_title: str = "Generate Yields"
    template_name: str = "accounts/yields.html"

    def post(self, request, *args, **kwargs):
        tax = request.POST.get("tax")
        result = SavingsAccount.generate_yield_for_savings_accounts(tax)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse_lazy('accounts:list')

class SearchAccountsView(TemplateTitleMixin, CurrentYearMixin, GetAccountMultipleTypesMixin, TemplateView):
    template_title: str = "Search Accounts"
    template_name: str = "accounts/search.html"
    model : Account
    def post(self, request, *args, **kwargs):
        account_number = request.POST["account_number"]
        try:
            account = self.get_account_by_number(account_number)
            self.object = account
            return HttpResponseRedirect(self.get_success_url())
        except:
            reason: str = "Failed retrieving account information."
            messages.error(self.request, reason, extra_tags="danger")
            return self.render_to_response(self.get_context_data())
    def get_success_url(self) -> str:
            return reverse_lazy('accounts:detail', kwargs={"number": self.object.number})