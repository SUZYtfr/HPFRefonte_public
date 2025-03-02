from rest_framework.routers import SimpleRouter
from .views import (
    PrivateImageViewSet,
    PrivateBannerViewSet,
)

app_name = "images"

image_router = SimpleRouter()
image_router.register("contentimages", PrivateImageViewSet, basename="private-contentimages")
image_router.register("banners", PrivateBannerViewSet, basename="private-banners")

urlpatterns = image_router.urls
