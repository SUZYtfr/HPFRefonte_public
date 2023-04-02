from rest_framework.routers import SimpleRouter
from rest_framework.urls import path
from django.urls import include

from .views import NewsViewSet, NewsCommentViewSet

app_name = "news"

news_router = SimpleRouter()
news_router.register(r"", NewsViewSet, basename="news")
newscomments_router = SimpleRouter()
newscomments_router.register(r"", NewsCommentViewSet, basename="comment")

urlpatterns = [
    path(
        r"<int:news_pk>/comments/", include(newscomments_router.urls),
    )
] + news_router.urls
