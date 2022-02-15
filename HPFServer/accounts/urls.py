from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import AccountCreationView, AccountManagementView

app_name = "accounts"

urlpatterns = [
    path(r"", AccountCreationView.as_view()),
    path(r"token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(r"token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(r"profile/", AccountManagementView.as_view(), name="manage"),
]
