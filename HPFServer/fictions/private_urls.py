from rest_framework.routers import SimpleRouter
from fictions.views import PrivateChapterViewSet, PrivateChapterTextVersionViewSet

app_name = "fictions"

fiction_router = SimpleRouter()
fiction_router.register(r"chapters", PrivateChapterViewSet)
fiction_router.register(r"versions", PrivateChapterTextVersionViewSet)

urlpatterns = fiction_router.urls
