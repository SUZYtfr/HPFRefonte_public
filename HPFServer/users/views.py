from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import PublicUserSerializer, UserCardSerializer

from .models import User


# VUES PUBLIQUES

class PublicUserViewSet(ReadOnlyModelViewSet):
    """Ensemble de vues publiques pour les membres"""

    serializer_class = PublicUserSerializer
    search_fields = ("nickname",)

    def get_queryset(self):
        """Détermine la liste de membres à afficher
        Un utilisateur affiche les membres actifs, un modérateur affiche tous les membres."""

        if self.request.user.has_perm("users.user_list_full_view"):
            return User.objects.all().order_by("nickname")
        else:
            return User.active.all().order_by("nickname")

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return UserCardSerializer

        return self.serializer_class
