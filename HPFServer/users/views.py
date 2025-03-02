from rest_framework import viewsets, mixins
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_501_NOT_IMPLEMENTED, HTTP_403_FORBIDDEN
from django_filters.rest_framework.backends import DjangoFilterBackend
from django.db import transaction
from django.utils import timezone

from users.models import User, Theme
from users.filters import UserFilterSet
from users.serializers import UserSerializer, UserListSerializer, ThemeSerializer


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


class PrivateThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    @transaction.atomic
    def perform_create(self, serializer: ThemeSerializer):
        if serializer.validated_data["default"] == True:
            Theme.objects.update(default=False)
        return super().perform_update(serializer)
    
    @transaction.atomic
    def perform_update(self, serializer: ThemeSerializer):
        if serializer.validated_data["default"] == True:
            Theme.objects.update(default=False)
        return super().perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        theme = self.get_object()
        if theme.default:
            return Response(
                status=HTTP_403_FORBIDDEN,
                data="Le thème par défaut ne peut pas être supprimé.",
            )
        return super().destroy(request, *args, **kwargs)


class PublicThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.exclude(
        enabled=False,
    ).exclude(
        use_default_from__gt=timezone.now(),
    ).exclude(
        use_default_to__lt=timezone.now(),
    )
    serializer_class = ThemeSerializer
