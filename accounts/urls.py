from django.urls import path

from accounts.apps import AccountsConfig
from accounts.views import CreateAccountView
from accounts.views import DetailAccountView
from accounts.views import ListAccountView
from accounts.views import MakeDepositView
from accounts.views import MakeTransferView
from accounts.views import MakeWithdrawView
from accounts.views import GenerateYieldsView
from accounts.views import SearchAccountsView

app_name = AccountsConfig.name

urlpatterns = [
    path("", ListAccountView.as_view(), name="list"),
    path("create/", CreateAccountView.as_view(), name="create"),
    path("<int:number>/", DetailAccountView.as_view(), name="detail"),
    path("<int:number>/deposit/", MakeDepositView.as_view(), name="deposit"),
    path("<int:number>/transfer/", MakeTransferView.as_view(), name="transfer"),
    path("<int:number>/withdraw/", MakeWithdrawView.as_view(), name="withdraw"),
    path("yields/", GenerateYieldsView.as_view(), name="yields"),
    path("search/", SearchAccountsView.as_view(), name="search")
]