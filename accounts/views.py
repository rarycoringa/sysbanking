from typing import List
from typing import Dict

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView

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