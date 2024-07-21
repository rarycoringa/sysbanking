from django.urls import path

from restapi.apps import RestAPIConfig
from restapi.views import AccountListAPIView
from restapi.views import AccountDetailAPIView
from restapi.views import AccountDepositAPIView
from restapi.views import AccountWithdrawAPIView
from restapi.views import AccountTransferAPIView
from restapi.views import GenerateYieldAPIView

app_name = RestAPIConfig.name

urlpatterns = [
    path("accounts", AccountListAPIView.as_view()),
    path("accounts/<int:number>", AccountDetailAPIView.as_view()),
    path("accounts/<int:number>/deposit", AccountDepositAPIView.as_view()),
    path("accounts/<int:number>/transfer", AccountTransferAPIView.as_view()),
    path("accounts/<int:number>/withdraw", AccountWithdrawAPIView.as_view()),
    path("accounts/yields", GenerateYieldAPIView.as_view()),
]