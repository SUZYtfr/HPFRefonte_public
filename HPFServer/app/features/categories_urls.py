from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet

app_name = "categories"

category_router = SimpleRouter()
category_router.register(r"", CategoryViewSet, basename="category")

urlpatterns = category_router.urls
