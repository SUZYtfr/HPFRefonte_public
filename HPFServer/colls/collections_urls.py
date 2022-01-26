from rest_framework.routers import SimpleRouter

from .views import PublicCollectionViewSet


app_name = "collections"

collections_router = SimpleRouter()
collections_router.register(r"", PublicCollectionViewSet, basename="collection")


# Redéfinition crasseuse de la fonction de correspondance d'URL du routeur
def get_esthetic_lookup_regex(viewset, lookup_prefix=''):
    return r"(?P<collection_id>\d+)(-.+)?"


collections_router.get_lookup_regex = get_esthetic_lookup_regex


urlpatterns = collections_router.urls
