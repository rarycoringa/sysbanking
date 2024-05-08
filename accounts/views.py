from typing import Dict
from typing import List
from typing import Union
from typing import Callable

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

from accounts.mixins import CurrentYearMixin
from accounts.mixins import TemplateTitleMixin
from accounts.models import Account


class ListAccountView(CurrentYearMixin, TemplateTitleMixin, ListView):
    context_object_name: str = "accounts"
    model: Account = Account
    template_name: str = "accounts/list.html"
    template_title: str = "Account List"


class DetailAccountView(CurrentYearMixin, TemplateTitleMixin, DetailView):
    context_object_name: str = "account"
    model: Account = Account
    slug_field: str = "number"
    slug_url_kwarg: str = "number"
    template_name: str = "accounts/detail.html"
    template_title: str = "Account Details"
    

class CreateAccountView(SuccessMessageMixin, CurrentYearMixin, TemplateTitleMixin, CreateView):
    fields: List[str] = ["number"]
    model: Account = Account
    success_url = reverse_lazy('accounts:create')
    template_name: str = "accounts/create.html"
    template_title: str = "Create Accounts"

    def get_success_message(self, cleaned_data: Dict[str, str]) -> str:
        account: Account = self.object
        return f"Account Nº {account.number} was successfully created."

class TransactionView(DetailView):
    transaction_name: str = None
    transaction_parameters_names: List[str] = None

    def transaction_valid(self, message: str = "Transaction sucessfully completed.") -> HttpResponseRedirect:
        """If the form is valid, redirect to the supplied URL."""
        messages.success(self.request, message, extra_tags="success")

        return HttpResponseRedirect(self.get_success_url())

    def transaction_invalid(self, reason: str = "Failed trying to do transaction.") -> HttpResponse:
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, reason, extra_tags="danger")

        return self.render_to_response(self.get_context_data())

    def post(self, request: HttpRequest, *args, **kwargs) -> Union[HttpResponse, HttpResponseRedirect]:
        self.object: Account = self.get_object()

        transaction_parameters: Dict[str, str] = {
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
        return reverse_lazy('accounts:deposit', kwargs={"number": self.object.number})

class MakeTransferView(TemplateTitleMixin, CurrentYearMixin, TransactionView):
    context_object_name: str = "account"
    model: Account = Account
    slug_field: str = "number"
    slug_url_kwarg: str = "number"
    template_name: str = "accounts/transfer.html"
    template_title: str = "Transfer"
    transaction_name: str  = "transfer"
    transaction_parameters_names: List[str] = ["amount", "to_account"]

    def get_success_url(self) -> str:
        return reverse_lazy('accounts:transfer', kwargs={"number": self.object.number})

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
        return reverse_lazy('accounts:withdraw', kwargs={"number": self.object.number})