from rest_framework.routers import SimpleRouter
from .views import ChapterViewSet

app_name = "chapters"

chapter_router = SimpleRouter()
chapter_router.register(r"", ChapterViewSet, basename="chapter")

urlpatterns = chapter_router.urls
