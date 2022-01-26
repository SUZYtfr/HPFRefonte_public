from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import BannerSerializer
from .models import Banner


class BannerViewSet(ModelViewSet):
    """Ensemble de vues publiques pour les bannières"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)
