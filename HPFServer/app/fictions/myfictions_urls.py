from rest_framework.routers import SimpleRouter

from .views import MyFictionsViewSet, MyChapterViewSet
from django.urls import path, re_path

app_name = "myfictions"


myfiction_router = SimpleRouter()
myfiction_router.register(r"", MyFictionsViewSet, basename="myfiction")

urlpatterns = [
    re_path(r"^(?P<pk>\d+)/chapitres/$", MyChapterViewSet.as_view(actions={"post": "create"}),
            name="myfiction-chapter-list"),
]

urlpatterns += myfiction_router.urls
