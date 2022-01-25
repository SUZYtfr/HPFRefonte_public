from django.urls import path

from fictions.views import BetaViewSet

app_name = "betas"

urlpatterns = [
    path(r"", BetaViewSet.as_view(actions={"get": "list",
                                           "post": "create"}),
         name="beta-list"),
    path(r"<pk>/", BetaViewSet.as_view(actions={"get": "retrieve",
                                                "put": "update"}),
         name="beta-detail"),
]