from rest_framework.routers import SimpleRouter

from users.views import PrivateUserViewSet, PrivateThemeViewSet


app_name = "users"

users_router = SimpleRouter()
users_router.register(r"users", viewset=PrivateUserViewSet, basename=r"user")
theme_router = SimpleRouter()
theme_router.register(r"themes", viewset=PrivateThemeViewSet, basename=r"theme")

urlpatterns = users_router.urls + theme_router.urls
