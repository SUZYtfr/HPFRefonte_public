from rest_framework.routers import SimpleRouter

from users.views import UserViewSet


app_name = "users"

users_router = SimpleRouter()
users_router.register(r"", viewset=UserViewSet, basename=r"user")

urlpatterns = users_router.urls
