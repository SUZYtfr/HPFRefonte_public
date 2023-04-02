from rest_framework.routers import SimpleRouter

from .views import CollectionViewSet


app_name = "collections"

collections_router = SimpleRouter()
collections_router.register(r"", CollectionViewSet, basename="collection")

urlpatterns = collections_router.urls
