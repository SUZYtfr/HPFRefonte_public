from django.utils import timezone

from rest_framework import viewsets, decorators, response, status, permissions

from .serializers import (
    CharacteristicSerializer,
    StaffCharacteristicSerializer,
    StaffCharacteristicTypeSerializer,
    StaffCharacteristicOrderSerializer,
)
from .models import Characteristic, CharacteristicType
from core.permissions import DjangoPermissionOrReadOnly


class DjangoPermissionOrCreateOnly(DjangoPermissionOrReadOnly):
    """Permission autorisant la création"""

    def has_permission(self, request, view):
        if request.method in [*permissions.SAFE_METHODS, "POST"]:
            return True
        elif self.has_django_permissions(view, request):
            return True
        return False


class CharacteristicViewSet(viewsets.ModelViewSet):
    """Ensemble de vues publiques pour les caractéristiques"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, DjangoPermissionOrCreateOnly]
    serializer_class = CharacteristicSerializer
    queryset = Characteristic.objects.allowed().fiction_counts().order_by("-fiction_count")
    search_fields = ["name"]

    def get_queryset(self):
        """Détermine la liste de caractéristiques à afficher"""

        if self.request.user.is_staff:  # TODO - characteristics.view_characteristics
            return Characteristic.objects.order_by("characteristic_type")
        return self.queryset

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.request.user.is_staff:  # TODO - characteristics.view_characteristics
            return StaffCharacteristicSerializer
        return self.serializer_class

    @decorators.action(
        detail=False,
        methods=["POST"],
        url_name="upsert",
        name="Characteristic create or retrieve",
        url_path="upsert",
    )
    def create_or_retrieve(self, request, *args, **kwargs):
        """Traite la requête de création ou récupération de la caractéristique"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_create_or_retrieve(serializer)
        headers = self.get_success_headers(serializer.data)
        characteristic_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return response.Response(serializer.data, status=characteristic_status, headers=headers)

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())

    def perform_create_or_retrieve(self, serializer):
        """Finalise l'action de création ou récupération de la caractéristique"""

        instance, created = serializer.save(
            upsert=True,
            creation_user=self.request.user,
            creation_date=timezone.now(),
        )
        return created


class CharacteristicTypeViewSet(viewsets.ModelViewSet):
    """Ensemble de vues de modération pour les types de caractéristiques"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, DjangoPermissionOrReadOnly]
    queryset = CharacteristicType.objects.all()
    serializer_class = StaffCharacteristicTypeSerializer

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())

    @decorators.action(
        detail=True,
        methods=["GET", "PUT"],
        serializer_class=StaffCharacteristicOrderSerializer,
        url_name="characteristic-order",
    )
    def order(self, request, *args, **kwargs):
        if request.method == "GET":
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response.Response(serializer.data)
        elif request.method == "PUT":
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.reorder()

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return response.Response(serializer.data)
