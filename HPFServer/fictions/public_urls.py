from rest_framework.routers import SimpleRouter

from .views import CollectionViewSet, FictionViewSet, PublicChapterViewSet

app_name = "fictions"

fiction_router = SimpleRouter()
fiction_router.register(r"fictions", FictionViewSet)
fiction_router.register(r"chapters", PublicChapterViewSet)
fiction_router.register(r"collections", CollectionViewSet)

urlpatterns = fiction_router.urls
