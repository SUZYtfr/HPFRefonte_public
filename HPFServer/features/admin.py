from django.contrib import admin
from core.admin import BaseAdminAccess

from .models import Category, Feature


class CategoryAdminAccess(BaseAdminAccess):
    """Accès d'administration aux catégories"""

    ordering = ("id",)
    list_display = ("name", "min_limit", "max_limit",)
    readonly_fields = ("creation_user", "modification_user", "creation_date", "modification_date",)

    # # Les administrateurs ne peuvent pas ajouter de catégorie de caractéristiques
    # def has_add_permission(self, request):
    #     return False


class FeatureAdminAccess(BaseAdminAccess):
    """Accès d'administration aux caractéristiques"""

    ordering = ("-id",)
    list_display = ("id", "name", "category", "is_personal", "is_forbidden",)
    list_display_links = ("name", "id",)
    list_filter = ("category", "is_personal", "is_forbidden",)
    fieldsets = (
        ("Caractéristique", {"fields": ("name", "description", "category", "parent", "is_personal")}),
        ("Métadonnées", {"fields": (("creation_user", "creation_date",),
                                    ("modification_user", "modification_date",))})
    )
    readonly_fields = ("creation_user", "modification_user", "creation_date", "modification_date",)


admin.site.register(Category, CategoryAdminAccess)
admin.site.register(Feature, FeatureAdminAccess)
