from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_501_NOT_IMPLEMENTED

from .models import User
from .serializers import UserSerializer, UserListSerializer
from .permissions import IsRequestUser, ReadOnly, HasPermission


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """Ensemble de vues pour les utilisateurs"""

    queryset = User.objects.active().order_by("username")
    serializer_class = UserSerializer
    # permission_classes = [IsRequestUser | HasPermission | ReadOnly]
    search_fields = ["username"]

    def get_queryset(self):
        """Détermine la liste de membres à afficher
        Un utilisateur affiche les membres actifs, un modérateur affiche tous les membres."""

        # if self.request.user.has_perm("users.view_user"):
        #     return User.objects.order_by("last_login")
        # return super().get_queryset()
        return User.objects.order_by("last_login")

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return UserListSerializer
        return super().get_serializer_class()

    @action(
        methods=["PUT"],
        detail=True,
        url_path="send-password-reset-email",
        serializer_class=None,
    )
    def send_password_reset_email(self, request: Request, *args, **kwargs) -> Response:
        return Response(status=HTTP_501_NOT_IMPLEMENTED)

    @action(
        methods=["PUT"],
        detail=True,
        serializer_class=None,        
    )
    def anonymise(self, request: Request, *args, **kwargs) -> Response:
        user: User = self.get_object()
        user.ban(anonymise=True)
        return Response()
