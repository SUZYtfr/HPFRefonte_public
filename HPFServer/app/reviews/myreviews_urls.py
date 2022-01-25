from .views import MyPersonalReviewsListView, MyPersonalReviewHistoryView, ReplyViewSet
from django.urls import path

app_name = "myreviews"

urlpatterns = [
    path(r"", MyPersonalReviewsListView.as_view(actions={"get": "list"})),
    path(r"<pk>/", MyPersonalReviewsListView.as_view(actions={"get": "retrieve",
                                                              "put": "update",
                                                              "patch": "partial_update",
                                                              "delete": "destroy"})),
    path(r"<pk>/historique/", MyPersonalReviewHistoryView.as_view()),
    path(r"<pk>/réponses/<reply_pk>/", ReplyViewSet.as_view(actions={"post": "create",
                                                                     "put": "update",
                                                                     "patch": "partial_update",
                                                                     "delete": "destroy"}),
         name="myreview-reply-detail"),
]