from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminAccess(UserAdmin):
    """Accès d'administration aux utilisateurs"""

    ordering = ("-id",)
    list_display = ("id", "username", "creation_date", "is_active", "is_premium", "is_staff", "is_superuser", "mean",)
    list_filter = ("creation_date", "is_premium", "is_active",)
    list_per_page = 20
    fieldsets = (
        ("Informations publiques", {"fields": ("nickname",
                                               "bio",
                                               "mean",)}),
        ("Informations privées", {"fields": ("gender",
                                             "birthdate",
                                             "realname",
                                             "email",)}),
        ("Préférences", {"fields": ("user_pref_font",
                                    "user_pref_font_size",
                                    "user_pref_line_spacing",
                                    "user_pref_dark_mode",
                                    "user_pref_skin",
                                    "user_pref_show_reaction",)}),
        ("Status et permissions", {"fields": (("is_active", "is_premium",),
                                              ("is_staff", "is_superuser",),
                                              "age_consent",)}),
        ("Groupes", {"classes": ("collapse",),
                     "fields": ("groups",)}),
        ("Métadonnées", {"description": "Ces informations sont protégées.",
                         "fields": (("creation_date", "modification_date",),
                                    "last_login",)}),
    )
    readonly_fields = ("creation_date", "modification_date", "last_login", "mean", "username",)
    search_fields = ("username",)

    # Par défaut, la page de création de nouvel utilisateur du panneau d'administration demande "username",
    # qui est réimplémenté manuellement dans mon modèle, et pas l'email, qui est obligatoire
    # Il faut redéfinir les infos obligatoires à demander dans le panneau
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nickname', "email", 'password1', 'password2'),
        }),
    )

    def has_nickname(self, obj):
        return bool(obj.nickname)
    has_nickname.short_description = "anonyme"

    def mean(self, obj):
        return obj.mean
    mean.short_description = "moyenne"

    def save_model(self, request, obj, form, change):
        """Finalise la modification de l'objet : le modificateur est l'utilisateur authentifié"""

        obj.modification_user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdminAccess)
