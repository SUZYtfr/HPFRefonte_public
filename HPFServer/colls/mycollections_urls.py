from rest_framework.routers import SimpleRouter
from .views import MyCollectionViewSet


app_name = "mycollections"


mycollections_router = SimpleRouter()
mycollections_router.register(r"", MyCollectionViewSet, basename="mycollection")

urlpatterns = mycollections_router.urls
