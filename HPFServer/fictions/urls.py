from rest_framework.routers import SimpleRouter
from rest_framework.urls import path
from django.urls import include

from .views import FictionViewSet, ChapterViewSet


app_name = "fictions"

fiction_router = SimpleRouter()
fiction_router.register(r"", FictionViewSet, basename="fiction")
chapter_router = SimpleRouter()
chapter_router.register(r"", ChapterViewSet, basename="chapter")

urlpatterns = [
    path(
        r"<fiction_pk>/chapters/", include(chapter_router.urls),
    )
] + fiction_router.urls
