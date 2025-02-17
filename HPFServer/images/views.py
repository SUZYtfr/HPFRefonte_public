from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework.backends import DjangoFilterBackend
from images.models import (
    Banner,
    ProfilePicture,
    ContentImage,
)
from images.serializers import (
    BannerSerializer,
    ProfilePictureSerializer,
    ContentImageSerializer,
    PrivateContentImageSerializer,
)
from images.filters import PrivateContentImageFilterSet, PrivateBannerFilterSet
from core.utils import get_moderation_account


class BannerViewSet(viewsets.ModelViewSet):
    """Ensemble de vues publiques pour les bannières"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrivateBannerFilterSet

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())


class PrivateBannerViewSet(viewsets.ModelViewSet):
    """Ensemble de vues privées pour les bannières"""

    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrivateBannerFilterSet

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


class PrivateImageViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    # permission_classes = [IsStaff]
    queryset = ContentImage.objects.all()
    serializer_class = PrivateContentImageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PrivateContentImageFilterSet 

    def perform_update(self, serializer):
        # user = self.request.user
        user = get_moderation_account()
        serializer.save(
            modification_user=user,
            modification_date=timezone.now(),
        )

    @action(
        detail=True,
        methods=["PUT"],
        url_name="remove-image",
        url_path="remove-image",
    )
    def remove_image(self, request, *args, **kwargs):
        """Supprime l'URI de l'image et l'image du système de fichiers le cas échéant"""
        
        image = self.get_object()
        image.src_url = None
        image.src_path.delete(save=False)
        image.src_path = None
        image.save()
        return Response()
