from rest_framework.urls import path
from rest_framework.routers import SimpleRouter

from .views import NewsListView, NewsCommentViewSet

app_name = "news"

newscomments_router = SimpleRouter()
newscomments_router.register(r"comments", NewsCommentViewSet)

urlpatterns = [
    path(r"", NewsListView.as_view(), name="news-list"),
] + newscomments_router.urls
