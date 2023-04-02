from rest_framework.urls import path
from rest_framework.routers import SimpleRouter
from django.urls import include

from .views import ReplyViewSet, FictionReviewViewSet, ChapterReviewViewSet, CollectionReviewViewSet


app_name = "reviews"

review_router = SimpleRouter()
review_router.register(r"fictions", FictionReviewViewSet, basename="fiction-review")
review_router.register(r"chapters", ChapterReviewViewSet, basename="chapter-review")
review_router.register(r"collections", CollectionReviewViewSet, basename="collection-review")
reply_router = SimpleRouter()
reply_router.register(r"", ReplyViewSet, basename="reply")


urlpatterns = [
    path(r"fictions/<review_pk>/replies/", include(reply_router.urls)),
    path(r"chapters/<review_pk>/replies/", include(reply_router.urls)),
    path(r"collections/<review_pk>/replies/", include(reply_router.urls)),
] + review_router.urls
