from rest_framework.urls import path
from rest_framework.routers import SimpleRouter
from django.urls import include

from .views import ModelReviewListView, ObjectReviewListCreateView, ReviewsViewSet, ReplyViewSet


app_name = "reviews"

general_review_router = SimpleRouter()
general_review_router.register(r"", ReviewsViewSet, basename="review")
object_review_router = SimpleRouter()
object_review_router.register(r"", ObjectReviewListCreateView, basename="object-review")
reply_router = SimpleRouter()
reply_router.register(r"", ReplyViewSet, basename="reply")

# TODO - à fusionner si possible
urlpatterns = [
    path(r"fictions/", ModelReviewListView.as_view(), kwargs={"model_name": "fiction"}),
    path(r"fictions/<object_pk>/", include((object_review_router.urls, "fictions")), kwargs={"model_name": "fiction"}),
    path(r"chapters/", ModelReviewListView.as_view(), kwargs={"model_name": "chapter"}),
    path(r"chapters/<object_pk>/", include((object_review_router.urls, "chapters")), kwargs={"model_name": "chapter"}),
    path(r"collections/", ModelReviewListView.as_view(), kwargs={"model_name": "collection"}),
    path(r"collections/<object_pk>", include((object_review_router.urls, "collections")), kwargs={"model_name": "collection"}),
    path(r"users/", ModelReviewListView.as_view(), kwargs={"model_name": "user"}),
    path(r"users/<object_pk>/", include((object_review_router.urls, "users")), kwargs={"model_name": "user"}),
    path(r"<review_pk>/replies/", include(reply_router.urls))
] + general_review_router.urls
