from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User, UserProfile, UserPreferences


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    exclude = ["bio_images"]
    readonly_fields = ["modification_user"]
    classes = ["collapse"]


class UserPreferencesInline(admin.StackedInline):
    model = UserPreferences
    classes = ["collapse"]


@admin.register(User)
class UserAdminPage(UserAdmin):
    """Accès d'administration des utilisateurs"""

    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "username", "is_active", "first_seen", "last_login"]
    list_display_links = ["username"]
    list_filter = ["is_active"]
    search_fields = ["username"]
    fieldsets = [
        (None, {
            "fields": ("username", "email"),
        }),
        ("Status", {
            "fields": ("is_active", "is_staff", "is_superuser"),
        }),
        ("Métadonnées", {
            "fields": ("first_seen", "last_login"),
        })
    ]
    inlines = [UserProfileInline, UserPreferencesInline]
    readonly_fields = ["first_seen", "last_login"]

    # Par défaut, la page de création de nouvel utilisateur du panneau d'administration demande "username",
    # qui est réimplémenté manuellement dans mon modèle, et pas l'email, qui est obligatoire
    # Il faut redéfinir les infos obligatoires à demander dans le panneau
    add_fieldsets = [
        (None, {
            "fields": ("username", "email", "password1", "password2"),
            "classes": ["wide"],
        }),
    ]
