from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import (
    Banner,
    ProfilePicture,
    ContentImage,
)
from .serializers import (
    BannerSerializer,
    ProfilePictureSerializer,
    ContentImageSerializer,
)


class BannerViewSet(viewsets.ModelViewSet):
    """Ensemble de vues publiques pour les bannières"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())


class ProfilePictureView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProfilePictureSerializer
    queryset = ProfilePicture.objects.all()

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())


class ContentImageViewSet(viewsets.ModelViewSet):
    serializer_class = ContentImageSerializer
    queryset = ContentImage.objects.all()
