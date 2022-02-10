from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .serializers import FeatureSerializer, StaffFeatureSerializer, StaffCategorySerializer, StaffFeatureOrderSerializer
from .models import Feature, Category


class IsStaffOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in [*SAFE_METHODS, "POST"]:
            return True
        if request.user.is_staff:
            return True
        return False


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class FeatureViewSet(ModelViewSet):
    """Ensemble de vues publiques pour les caractéristiques"""

    permission_classes = (IsAuthenticatedOrReadOnly, IsStaffOrCreateOnly,)
    serializer_class = FeatureSerializer
    queryset = Feature.objects.exclude(is_forbidden=True).order_by("category")
    search_fields = ("name",)

    def get_queryset(self):
        """Détermine la liste de caractéristiques à afficher"""
        if self.request.user.is_staff:
            return Feature.objects.order_by("category")
        return self.queryset

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""
        if self.request.user.is_staff:
            return StaffFeatureSerializer
        return self.serializer_class

    # Crée le tag ou renvoie le tag existant
    @action(methods=["POST"], detail=False, url_name="upsert", name="Feature create or retrieve", url_path="upsert")
    def create_or_retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created = self.perform_create_or_retrieve(serializer)
        headers = self.get_success_headers(serializer.data)
        feature_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=feature_status, headers=headers)

    def perform_create_or_retrieve(self, serializer):
        instance, created = serializer.save(upsert=True)
        return created


class CategoryViewSet(ModelViewSet):
    """Ensemble de vues de modération pour les catégories"""

    permission_classes = (IsAuthenticated, IsStaff)
    queryset = Category.objects
    serializer_class = StaffCategorySerializer

    @action(methods=["GET", "PUT"], detail=True, serializer_class=StaffFeatureOrderSerializer, url_name="feature-order")
    def order(self, request, *args, **kwargs):
        if request.method == "GET":
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
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

            return Response(serializer.data)
