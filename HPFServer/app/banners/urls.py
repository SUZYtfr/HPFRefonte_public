from rest_framework.routers import SimpleRouter
from .views import BannerViewSet

app_name = "banners"

banner_router = SimpleRouter()
banner_router.register(r"", BannerViewSet, basename="banner")

urlpatterns = banner_router.urls
