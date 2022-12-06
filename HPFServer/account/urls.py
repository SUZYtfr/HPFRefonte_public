from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AuthenticatedUserView

app_name = "account"

urlpatterns = [
    path(r"", AuthenticatedUserView.as_view(), name="current_user"),
    path(r"token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(r"token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
