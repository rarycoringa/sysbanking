from django.urls import path

from accounts.apps import AccountsConfig
from accounts.views import CreateAccountView
from accounts.views import DetailAccountView
from accounts.views import ListAccountView
from accounts.views import MakeDepositView

app_name = AccountsConfig.name

urlpatterns = [
    path("", ListAccountView.as_view(), name="list"),
    path("create/", CreateAccountView.as_view(), name="create"),
    path("<int:number>/", DetailAccountView.as_view(), name="detail"),
    path("<int:number>/deposit/", MakeDepositView.as_view(), name="deposit"),
]