from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from core.permissions import DjangoPermissionOrReadOnly
from .models import Fiction


class IsParentFictionAuthorOReadOnly(DjangoPermissionOrReadOnly):
    """Permission autorisant le contrôle d'un chapitre par l'auteur de sa fiction parente"""

    def has_permission(self, request, view):
        if super(IsParentFictionAuthorOReadOnly, self).has_permission(request, view):
            return True
        elif request.user in get_object_or_404(Fiction, pk=view.kwargs["fiction_pk"]).authors.all():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if super(IsParentFictionAuthorOReadOnly, self).has_object_permission(request, view, obj):
            return True
        elif request.user in obj.fiction.authors.all():
            return True
        return False


class HasStaffValidation(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm("fictions.staff_validation"):
            return True
        return False


class IsFictionAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.user in get_object_or_404(Fiction, pk=view.kwargs["fiction_pk"]).authors.all():
            return True
        return False


class IsFictionFirstAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.user == obj.authors.first():
            return True
        return False