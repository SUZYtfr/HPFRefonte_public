from django.urls import include
from rest_framework.urls import path

from rest_framework.routers import SimpleRouter
from .views import FeatureViewSet, CategoryViewSet

app_name = "features"

feature_router = SimpleRouter()
feature_router.register(r"", FeatureViewSet, basename="feature")
category_router = SimpleRouter()
category_router.register(r"", CategoryViewSet, basename="category")


urlpatterns = [
    path(
        r"categories/", include(category_router.urls),
    )
] + feature_router.urls

