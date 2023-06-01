from django.contrib import admin
from core.admin import BaseAdminAccess

from .models import CharacteristicType, Characteristic


class CharacteristicTypeAdminAccess(BaseAdminAccess):
    """Accès d'administration aux types de caractéristiques"""

    ordering = ("id",)
    list_display = ("name", "min_limit", "max_limit",)
    readonly_fields = ("creation_user", "modification_user", "creation_date", "modification_date",)

    # # Les administrateurs ne peuvent pas ajouter de types de caractéristiques
    # def has_add_permission(self, request):
    #     return False


class CharacteristicAdminAccess(BaseAdminAccess):
    """Accès d'administration aux caractéristiques"""

    ordering = ("-id",)
    list_display = ("id", "name", "characteristic_type", "is_personal", "is_forbidden",)
    list_display_links = ("name", "id",)
    list_filter = ("characteristic_type", "is_personal", "is_forbidden",)
    fieldsets = (
        ("Caractéristique", {"fields": ("name", "description", "characteristic_type", "parent", "is_personal")}),
        ("Métadonnées", {"fields": (("creation_user", "creation_date",),
                                    ("modification_user", "modification_date",))})
    )
    readonly_fields = ("creation_user", "modification_user", "creation_date", "modification_date",)


admin.site.register(CharacteristicType, CharacteristicTypeAdminAccess)
admin.site.register(Characteristic, CharacteristicAdminAccess)
