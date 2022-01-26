from rest_framework.routers import SimpleRouter
from .views import FeatureViewSet

app_name = "features"

feature_router = SimpleRouter()
feature_router.register(r"", FeatureViewSet, basename="feature")

urlpatterns = feature_router.urls
