from rest_framework.routers import SimpleRouter
from rest_framework.urls import path
from django.urls import include

from .views import FictionViewSet, ChapterViewSet


app_name = "fictions"

fiction_router = SimpleRouter()
fiction_router.register(r"", FictionViewSet, basename="fiction")

urlpatterns = fiction_router.urls + [
    path(r"<pk>/chapters/", include([
        path(r"", ChapterViewSet.as_view(actions={"get": "list",
                                                  "post": "create"}),
             name="chapter-list"),
        path(r"<chapter_pk>/", ChapterViewSet.as_view(actions={"get": "retrieve",
                                                               "put": "update",
                                                               "patch": "partial_update",
                                                               "delete": "destroy"}),
             name="chapter-detail"),
        path(r"<chapter_pk>/validation/", ChapterViewSet.as_view(actions={"put": "submit"}),
             name="chapter-submit"),
        ]))
]
