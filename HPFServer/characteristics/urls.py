from rest_framework.routers import SimpleRouter
from .views import CharacteristicViewSet, CharacteristicTypeViewSet

app_name = "characteristics"

characteristic_router = SimpleRouter()
characteristic_router.register(r"characteristics", CharacteristicViewSet, basename="characteristic")
characteristic_router.register(r"characteristic-types", CharacteristicTypeViewSet, basename="characteristictype")

urlpatterns = characteristic_router.urls

