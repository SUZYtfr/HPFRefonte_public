from rest_framework.routers import SimpleRouter
from .views import (
    BannerViewSet,
    ProfilePictureView,
    ContentImageViewSet,
)

app_name = "images"

image_router = SimpleRouter()
image_router.register(r"banners", BannerViewSet, basename="banner")
image_router.register(r"profilepictures", ProfilePictureView, basename="profilepicture")
image_router.register(r"contentimages", ContentImageViewSet, basename="contentimage")

urlpatterns = image_router.urls
