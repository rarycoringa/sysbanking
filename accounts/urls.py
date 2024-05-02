from django.urls import path

from accounts.views import CreateAccountView
from accounts.apps import AccountsConfig

app_name = AccountsConfig.name

urlpatterns = [
    path("create/", CreateAccountView.as_view(), name="create")
]