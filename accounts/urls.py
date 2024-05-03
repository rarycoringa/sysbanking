from django.urls import path

from accounts.apps import AccountsConfig
from accounts.views import CreateAccountView
from accounts.views import DetailAccountView
from accounts.views import ListAccountView

app_name = AccountsConfig.name

urlpatterns = [
    path("", ListAccountView.as_view(), name="list"),
    path("<int:number>/", DetailAccountView.as_view(), name="detail"),
    path("create/", CreateAccountView.as_view(), name="create"),
]