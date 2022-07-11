from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins, decorators

from .models import User, UserProfile, UserPreferences
from .serializers import (
    UserSerializer,
    UserStaffSerializer,
    UserProfileSerializer,
    UserPreferencesSerializer,
)
from .permissions import IsRequestUser, ReadOnly, HasPermission


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    """Ensemble de vues publiques pour les utilisateurs"""

    queryset = User.objects.active().order_by("nickname")
    serializer_class = UserSerializer
    permission_classes = [IsRequestUser | HasPermission | ReadOnly]
    search_fields = ["nickname"]

    def get_queryset(self):
        """Détermine la liste de membres à afficher
        Un utilisateur affiche les membres actifs, un modérateur affiche tous les membres."""

        if self.request.user.has_perm("users.view_user"):
            return User.objects.order_by("last_login")
        return self.queryset

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.request.user.has_perm("users.view_user"):
            return UserStaffSerializer
        return self.serializer_class

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)

    @decorators.action(
        methods=["PUT"],
        detail=True,
        url_path="profile",
        name="profil",
        serializer_class=UserProfileSerializer,
        permission_classes=[IsRequestUser | HasPermission]
    )
    def update_profile(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(UserProfile, pk=pk)
        serializer = self.get_serializer(profile, data=request.data)
        serializer.is_valid()
        serializer.save(modification_user=request.user)
        return self.retrieve(request, *args, **kwargs)

    @decorators.action(
        methods=["GET", "PUT"],
        detail=True,
        url_path="preferences",
        name="préférences",
        serializer_class=UserPreferencesSerializer,
        permission_classes=[IsRequestUser],
    )
    def manage_preferences(self, request, pk, *args, **kwargs):
        preferences = get_object_or_404(UserPreferences, pk=pk)
        if request.method == "PUT":
            serializer = self.get_serializer(preferences, data=request.data)
            serializer.is_valid()
            serializer.save(modification_user=request.user)
        return self.retrieve(request, *args, **kwargs)
