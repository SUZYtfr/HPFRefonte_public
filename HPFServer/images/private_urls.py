from rest_framework.routers import SimpleRouter
from .views import (
    PrivateImageViewSet,
)

app_name = "images"

image_router = SimpleRouter()
image_router.register("contentimages", PrivateImageViewSet, basename="private-contentimages")

urlpatterns = image_router.urls
