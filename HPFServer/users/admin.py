from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile, UserPreferences


class UserAdminAccess(UserAdmin):
    """Accès d'administration aux utilisateurs"""

    ordering = ("-id",)
    list_display = ("id", "username", "is_active", "is_staff", "is_superuser",)
    list_filter = ("is_active",)
    list_per_page = 20
    fields = [
        "username",
        "email",
        "is_active",
        "is_staff",
        "is_superuser",
        "first_seen",
        "last_login",
        "groups",
    ]
    fieldsets = ()
    readonly_fields = ("first_seen", "last_login")
    search_fields = ("username",)

    # Par défaut, la page de création de nouvel utilisateur du panneau d'administration demande "username",
    # qui est réimplémenté manuellement dans mon modèle, et pas l'email, qui est obligatoire
    # Il faut redéfinir les infos obligatoires à demander dans le panneau
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', "email", 'password1', 'password2'),
        }),
    )
    

admin.site.register(User, UserAdminAccess)
admin.site.register(UserProfile, admin.ModelAdmin)
admin.site.register(UserPreferences, admin.ModelAdmin)
