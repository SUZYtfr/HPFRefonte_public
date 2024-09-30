from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_501_NOT_IMPLEMENTED
from django_filters.rest_framework.backends import DjangoFilterBackend

from users.models import User
from users.filters import UserFilterSet
from users.serializers import UserSerializer, UserListSerializer


class PublicUserViewSet(viewsets.ReadOnlyModelViewSet):
    """Ensemble de vues publiques pour les utilisateurs"""
    queryset = User.objects.order_by("username")
    serializer_class = UserSerializer
    search_fields = ["username"]


class PrivateUserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """Ensemble de vues privées pour les utilisateurs"""

    queryset = User.objects.order_by("last_login")
    serializer_class = UserSerializer
    # permission_classes = [IsStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilterSet

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
