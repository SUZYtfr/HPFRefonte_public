from django.urls import path

from fictions.views import MyChapterViewSet

app_name = "mychapters"

urlpatterns = [
    path(r"", MyChapterViewSet.as_view(actions={"get": "list"}),
         name="mychapter-list"),
    path(r"<pk>/", MyChapterViewSet.as_view(actions={"get": "retrieve",
                                                     "put": "update",
                                                     "patch": "partial_update",
                                                     "delete": "destroy"}),
         name="mychapter-detail"),
    path(r"<pk>/validation/", MyChapterViewSet.as_view(actions={"put": "submit"}),
         name="mychapter-submit"),
]