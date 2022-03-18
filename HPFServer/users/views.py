from django.utils import timezone

from rest_framework.viewsets import *
from rest_framework.mixins import *
from rest_framework import permissions
from rest_framework.decorators import action

from core.permissions import DjangoPermissionOrReadOnly

from features.serializers import ShelvedElementSerializer

from .models import User
from .serializers import UserSerializer, UserCardSerializer


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """Ensemble de vues publiques pour les membres"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, DjangoPermissionOrReadOnly]
    serializer_class = UserSerializer
    search_fields = ["nickname"]
    queryset = User.objects.order_by("nickname")

    def get_queryset(self):
        """Détermine la liste de membres à afficher
        Un utilisateur affiche les membres actifs, un modérateur affiche tous les membres."""

        if self.request.user.has_perm("users.view_user"):
            return self.queryset
        return self.queryset.filter(is_active=True)

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return UserCardSerializer
        return self.serializer_class

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())

    @action(methods=["POST"], detail=True, url_path="add-to-bookshelf",
            serializer_class=ShelvedElementSerializer,
            permission_classes=[permissions.IsAuthenticated])
    def add_to_bookshelf(self, request, pk):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.save(work=self.get_object())
        return Response(serializer.data, status=201)
