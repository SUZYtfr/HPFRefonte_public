from rest_framework.routers import SimpleRouter

from users.views import PublicUserViewSet


app_name = "users"

users_router = SimpleRouter()
users_router.register(r"", viewset=PublicUserViewSet, basename=r"public-user")

urlpatterns = users_router.urls
