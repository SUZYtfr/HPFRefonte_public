from rest_framework.routers import SimpleRouter

from users.views import PublicUserViewSet, PublicThemeViewSet


app_name = "users"

users_router = SimpleRouter()
users_router.register(r"users", viewset=PublicUserViewSet, basename=r"public-user")
themes_router = SimpleRouter()
themes_router.register(r"themes", viewset=PublicThemeViewSet, basename=r"public-theme")

urlpatterns = users_router.urls + themes_router.urls
