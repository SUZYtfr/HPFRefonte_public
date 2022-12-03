from rest_framework.routers import SimpleRouter

from .views import FictionViewSet, ChapterViewSet

app_name = "fictions"

fiction_router = SimpleRouter()
fiction_router.register(r"fictions", FictionViewSet, basename="fiction")
fiction_router.register(r"chapters", ChapterViewSet, basename="chapter")

urlpatterns = fiction_router.urls
