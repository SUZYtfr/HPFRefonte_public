from django.contrib import admin
from core.admin import BaseAdminPage

from .models import CharacteristicType, Characteristic


@admin.register(CharacteristicType)
class CharacteristicTypeAdminPage(BaseAdminPage):
    """Page d'administration des types de caractéristiques"""

    ordering = ["id"]
    list_display = ["name", "min_limit", "max_limit"]
    fieldsets = [
        (None, {
            "fields": ["name", "min_limit", "max_limit"],
        }),
        ("Autres", {
            "fields": ["is_closed"],
            "classes": ["collapse"],
        })
    ]

    # # Les administrateurs ne peuvent pas ajouter de types de caractéristiques
    # def has_add_permission(self, request):
    #     return False


@admin.register(Characteristic)
class CharacteristicAdminPage(BaseAdminPage):
    """Page d'administration des caractéristiques"""

    ordering = ["-id"]
    list_display = ["id", "name", "characteristic_type"]
    list_display_links = ["name"]
    list_filter = ["characteristic_type"]
    search_fields = ["name"]
    fieldsets = [
        (None, {
            "fields": ["name", "description", "characteristic_type", "parent"],
        }),
        ("Autres", {
            "fields": ["is_personal", "is_highlighted", "is_forbidden", "replace_with"],
            "classes": ["collapse"],
        })
    ]
    autocomplete_fields = ["parent", "replace_with"]
