from rest_framework.routers import SimpleRouter
from .views import FeatureViewSet, CategoryViewSet

app_name = "features"

feature_router = SimpleRouter()
feature_router.register(r"features", FeatureViewSet, basename="feature")
feature_router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = feature_router.urls

