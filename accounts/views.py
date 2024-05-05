from typing import List
from typing import Dict

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.http import HttpRequest
from django.http import HttpResponseRedirect

from accounts.models import Account
from accounts.mixins import TemplateTitleMixin


class ListAccountView(TemplateTitleMixin, ListView):
    context_object_name: str = "accounts"
    model: Account = Account
    template_name: str = "accounts/list.html"
    template_title: str = "Account List"


class DetailAccountView(TemplateTitleMixin, DetailView):
    context_object_name: str = "account"
    model: Account = Account
    slug_field: str = "number"
    slug_url_kwarg: str = "number"
    template_name: str = "accounts/detail.html"
    template_title: str = "Account Details"
    

class CreateAccountView(SuccessMessageMixin, TemplateTitleMixin, CreateView):
    fields: List[str] = ["number"]
    model: Account = Account
    success_url = reverse_lazy('accounts:create')
    template_name: str = "accounts/create.html"
    template_title: str = "Create Accounts"

    def get_success_message(self, cleaned_data: Dict[str, str]) -> str:
        account: Account = self.object
        return f"Account Nº {account.number} was successfully created."

class TransactionView(DetailView):
    transaction_name: str  = None
    transaction_parameters_names: List[str] = None

    def transaction_valid(self):
        """If the form is valid, redirect to the supplied URL."""
        return HttpResponseRedirect(self.get_success_url())

    def transaction_invalid(self, reason: str):
        """If the form is invalid, render the invalid form."""
        messages.error(self.request, reason)

        return self.render_to_response(self.get_context_data())

    def post(self, request: HttpRequest, *args, **kwargs):
        self.object = self.get_object()

        transaction_parameters: Dict[str, str] = {
            param: request.POST[param]
            for param in self.transaction_parameters_names
        }
        
        transaction_method = self.object.__getattribute__(self.transaction_name)

        try:
            transaction_method(**transaction_parameters)
        except BaseException as err:
            return self.transaction_invalid(err)

        return self.transaction_valid()

class MakeDepositView(TemplateTitleMixin, TransactionView):
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

class MakeTransferView(TemplateTitleMixin, TransactionView):
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