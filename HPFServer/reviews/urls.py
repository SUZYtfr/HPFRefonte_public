from rest_framework.routers import SimpleRouter

from .views import (
    FictionReviewViewSet,
    ChapterReviewViewSet,
    CollectionReviewViewSet,
)

app_name = "reviews"

review_router = SimpleRouter()
review_router.register(r"fiction-reviews", FictionReviewViewSet, basename="fiction-review")
review_router.register(r"chapter-reviews", ChapterReviewViewSet, basename="chapter-review")
review_router.register(r"collection-reviews", CollectionReviewViewSet, basename="collection-review")

urlpatterns = review_router.urls
