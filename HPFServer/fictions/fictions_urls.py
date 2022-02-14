from rest_framework.routers import SimpleRouter

from .views import FictionViewSet


app_name = "fictions"

fiction_router = SimpleRouter()
fiction_router.register(r"", FictionViewSet, basename="fiction")

urlpatterns = fiction_router.urls
