from rest_framework.routers import SimpleRouter

from users.views import PrivateUserViewSet


app_name = "users"

users_router = SimpleRouter()
users_router.register(r"", viewset=PrivateUserViewSet, basename=r"user")

urlpatterns = users_router.urls
