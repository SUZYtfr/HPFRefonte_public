from django.urls import path

from .views import PublicAccountCreateView, PublicAccountLoginView, PrivateAccountManageView

app_name = "accounts"

urlpatterns = [
    path(r"", PublicAccountCreateView.as_view()),
    path(r"inscription/", PublicAccountCreateView.as_view(), name="create"),
    path(r"gestion/", PrivateAccountManageView.as_view(), name="manage"),
    path(r"connexion/", PublicAccountLoginView.as_view(), name="login"),
]
