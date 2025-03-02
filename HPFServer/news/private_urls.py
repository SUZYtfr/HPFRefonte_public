from rest_framework.routers import SimpleRouter
from rest_framework.urls import path
from django.urls import include

from .views import NewsCommentViewSet, PrivateNewsViewSet

app_name = "news"


news_router = SimpleRouter()
news_router.register(r"", PrivateNewsViewSet, basename="private-news")

urlpatterns = news_router.urls

# urlpatterns = [
#     path(
#         r"<int:news_pk>/comments/", include(newscomments_router.urls),
#     )
# ] + news_router.urls
