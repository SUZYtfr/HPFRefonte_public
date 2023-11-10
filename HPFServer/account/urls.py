from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from reviews.views import (
    AccountPublishedReviewViewset,
    AccountReceivedReviewViewset,
    AccountDraftReviewViewset,
    AccountUnansweredReviewViewset,
)
from .views import AuthenticatedUserView

app_name = "account"

account_reviews_router = SimpleRouter()
account_reviews_router.register("published-reviews", AccountPublishedReviewViewset, "published-review")
account_reviews_router.register("received-reviews", AccountReceivedReviewViewset, "received-review")
account_reviews_router.register("draft-reviews", AccountDraftReviewViewset, "draft-review")
account_reviews_router.register("unanswered-reviews", AccountUnansweredReviewViewset, "unanswered-review")

urlpatterns = [
    path(r"", AuthenticatedUserView.as_view(), name="current_user"),
    path(r"token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(r"token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + account_reviews_router.urls
