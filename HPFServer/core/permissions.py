from rest_framework import permissions
from fictions.models import Beta


class HasBetaTurnOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return \
            (obj.stage == Beta.BetaStage.REQUESTED and request.user == obj.user) or \
            (obj.stage == Beta.BetaStage.ONGOING and request.user == obj.user) or \
            (obj.stage == Beta.BetaStage.CORRECTED and request.user in obj.chapter.authors.all())


"""
Permissions hybrides, ou comment tirer profit du peu que Django permet en matière de permissions en palliant le peu
 que Django permet en matière de permissions...
has_permission() et has_object_permissions permettent toujours la lecture, et effectuent une vérification des
 permissions Django pour le reste.
De cette sorte, les permissions de base de Django ne sont plus applicables aux utilisateurs mais bien aux modérateurs
 (via des groupes par exemple): ainsi on passe d'un système de permissions sur modèles à permissions sur objets.
"""


class DjangoPermissionOrReadOnly(permissions.DjangoModelPermissions):
    """Permission de vérification des droits spéciaux de Django, ou lecture seule"""

    def has_django_permissions(self, view, request):
        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        return request.user.has_perms(perms)

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif self.has_django_permissions(view, request):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif self.has_django_permissions(view, request):
            return True
        return False


class IsObjectAuthorOrReadOnly(DjangoPermissionOrReadOnly):
    """Permission autorisant le contrôle d'un objet par son auteur"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if super(IsObjectAuthorOrReadOnly, self).has_object_permission(request, view, obj):
            return True
        elif request.user in obj.authors.all():
            return True
        return False


class IsObjectCreatorOrReadOnly(DjangoPermissionOrReadOnly):
    """Permission autorisant le contrôle d'un objet par son créateur"""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if super(IsObjectCreatorOrReadOnly, self).has_object_permission(request, view, obj):
            return True
        elif request.user == obj.creation_user:
            return True
        return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class HasPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        queryset = self._queryset(view)
        perms = self.get_required_permissions(request.method, queryset.model)
        return request.user.has_perms(perms)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
