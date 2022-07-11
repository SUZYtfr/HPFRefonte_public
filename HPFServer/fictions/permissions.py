# from django.shortcuts import get_object_or_404
from rest_framework import permissions
# from core.permissions import DjangoPermissionOrReadOnly
# from .models import Fiction


# class IsParentFictionAuthorOReadOnly(DjangoPermissionOrReadOnly):
#     """Permission autorisant le contrôle d'un chapitre par l'auteur de sa fiction parente"""
#
#     def has_permission(self, request, view):
#         if super(IsParentFictionAuthorOReadOnly, self).has_permission(request, view):
#             return True
#         elif request.user in get_object_or_404(Fiction, pk=view.kwargs["fiction_pk"]).authors.all():
#             return True
#         return False
#
#     def has_object_permission(self, request, view, obj):
#         if super(IsParentFictionAuthorOReadOnly, self).has_object_permission(request, view, obj):
#             return True
#         elif request.user in obj.fiction.authors.all():
#             return True
#         return False


class IsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class HasStaffValidation(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm("fictions.staff_validation"):
            return True
        return False


class IsFictionCoAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user in obj.coauthors.all():
            return True
        return False


class IsCreationUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creation_user


class IsParentFictionCreationUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsCreationUser().has_object_permission(request, view, obj.fiction)


class IsParentFictionCoAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return IsFictionCoAuthor().has_object_permission(request, view, obj.fiction)

#
# class IsFictionFirstAuthor(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method == "GET":
#             return True
#         if request.user == obj.authors.first():
#             return True
#         return False