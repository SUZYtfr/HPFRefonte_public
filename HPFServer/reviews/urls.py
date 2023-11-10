from rest_framework.routers import SimpleRouter

from .views import (
    FictionReviewViewset,
    ChapterReviewViewset,
    CollectionReviewViewset,
    AllReviewViewset,
    ReviewReplyViewset,
)

app_name = "reviews"

review_router = SimpleRouter()
review_router.register(r"fiction-reviews", FictionReviewViewset, basename="fiction-review")
review_router.register(r"chapter-reviews", ChapterReviewViewset, basename="chapter-review")
review_router.register(r"collection-reviews", CollectionReviewViewset, basename="collection-review")
review_router.register(r"all-reviews", AllReviewViewset, basename="all-review")
review_router.register(r"review-replies", ReviewReplyViewset, basename="review-reply")

urlpatterns = review_router.urls
