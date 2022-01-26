from .views import ReviewsOnMeListView, ReplyViewSet
from django.urls import path

app_name = "reviewsonme"

urlpatterns = [
    path(r"", ReviewsOnMeListView.as_view(actions={"get": "list"}),
         name="review-list"),
    path(r"<pk>/", ReviewsOnMeListView.as_view(actions={"get": "retrieve",
                                                        "post": "create"}),
         name="review-detail"),
    path(r"<pk>/réponses/", ReplyViewSet.as_view(actions={"post": "create"}),
         name="review-reply-list"),
    path(r"<pk>/réponses/<reply_pk>/", ReplyViewSet.as_view(actions={"post": "create",
                                                                     "put": "update",
                                                                     "patch": "partial_update",
                                                                     "delete": "destroy"}),
         name="review-reply-detail"),
]
