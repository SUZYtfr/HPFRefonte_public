from rest_framework.viewsets import *
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.permissions import DjangoPermissionOrReadOnly

from .models import User
from .serializers import UserSerializer, UserCardSerializer


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """Ensemble de vues publiques pour les membres"""

    permission_classes = [IsAuthenticatedOrReadOnly, DjangoPermissionOrReadOnly]
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
