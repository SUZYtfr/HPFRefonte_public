from rest_framework import viewsets, mixins

from .models import User
from .serializers import UserSerializer, UserListSerializer
from .permissions import IsRequestUser, ReadOnly, HasPermission


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    """Ensemble de vues pour les utilisateurs"""

    queryset = User.objects.active().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsRequestUser | HasPermission | ReadOnly]
    search_fields = ["username"]

    def get_queryset(self):
        """Détermine la liste de membres à afficher
        Un utilisateur affiche les membres actifs, un modérateur affiche tous les membres."""

        if self.request.user.has_perm("users.view_user"):
            return User.objects.order_by("last_login")
        return super().get_queryset()

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return UserListSerializer
        return super().get_serializer_class()

