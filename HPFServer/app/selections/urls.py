from rest_framework.urls import path
from rest_framework.routers import SimpleRouter
from .views import SelectionViewSet, PropositionCreationView

app_name = "selections"

selection_router = SimpleRouter()
selection_router.register("", SelectionViewSet)

urlpatterns = [
    path(r"<pk>/proposition/", PropositionCreationView.as_view()),
] + selection_router.urls
