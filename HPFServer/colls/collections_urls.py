from rest_framework.routers import SimpleRouter

from .views import PublicCollectionViewSet


app_name = "collections"

collections_router = SimpleRouter()
collections_router.register(r"", PublicCollectionViewSet, basename="collection")

urlpatterns = collections_router.urls
