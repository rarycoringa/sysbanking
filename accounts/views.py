from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.models import Account

class CreateAccountView(SuccessMessageMixin, CreateView):
    fields = ["number"]
    model = Account
    success_url = reverse_lazy('accounts:create')
    template_name = "accounts/create.html"

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        account: Account = self.object
        return f"Account Nº {account.number} was successfully created."