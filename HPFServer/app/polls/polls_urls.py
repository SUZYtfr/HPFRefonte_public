from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import PollViewSet, VoteView, ResultView

app_name = "polls"

poll_router = SimpleRouter()
poll_router.register("", PollViewSet, basename="poll")

urlpatterns = [
    path(r"<pk>/vote/", VoteView.as_view(), name="vote"),
    path(r"<pk>/results/", ResultView.as_view(), name="results")
] + poll_router.urls
