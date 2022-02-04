from rest_framework.routers import SimpleRouter
from .views import BannerViewSet, ProfilePictureView

app_name = "images"

banner_router = SimpleRouter()
banner_router.register(r"banners", BannerViewSet, basename="banner")

profilepictures_router = SimpleRouter()
profilepictures_router.register(r"profilepictures", ProfilePictureView, basename="profilepicture")

urlpatterns = banner_router.urls + profilepictures_router.urls
