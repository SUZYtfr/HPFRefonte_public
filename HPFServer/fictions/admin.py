from django.contrib import admin
from core.admin import BaseAdminAccess
from fictions.models import Fiction, Chapter, Beta


class FictionAdminAccess(BaseAdminAccess):
    """Accès d'administration aux fictions"""

    ordering = ("-id",)
    list_display = ("id", "title", "creation_date", "read_count", "word_count", "last_update_date", "status", "mean", "published",)
    list_per_page = 20
    list_filter = ("status", "creation_date",)

    fieldsets = (
        ("Détails", {"fields": ("title",
                                "storynote",
                                "summary",
                                "mean",
                                "status",
                                "featured",)}),
        ("Autorat", {"classes": ("collapse",),
                     "fields": ("authors",)}),
        ("Métadonnées", {"description": "Ces informations sont protégées.",
                         "fields": (("creation_user", "creation_date",),
                                    ("modification_user", "modification_date",),
                                    "published",
                                    "read_count",
                                    "word_count",
                                    "last_update_date",)}),
    )
    filter_horizontal = ("authors",)
    readonly_fields = ("creation_user", "creation_date", "modification_user", "modification_date",
                       "read_count", "last_update_date", "published", "mean", "word_count",)

    # Seulement pour fournir une traduction en français de la cellule et des valeurs pour True/False...
    def published(self, obj):
        return "Oui" if obj.is_published else "Non"
    published.short_description = "publiée"

    def mean(self, obj):
        return obj.mean
    mean.short_description = "moyenne"

    def word_count(self, obj):
        return obj.word_count
    word_count.short_description = "mots"

    def read_count(self, obj):
        return obj.read_count
    read_count.short_description = "lectures"


class ChapterAdminAccess(BaseAdminAccess):
    """Accès d'administration aux chapitres"""

    ordering = ("-id",)
    list_display = ("id", "title", "validation_status", "read_count", "word_count", "creation_date", "mean",)
    list_filter = ("validation_status", "creation_date")
    list_per_page = 20
    fieldsets = (
        ("Informations", {"fields": ("title",
                                     "startnote",
                                     "endnote",
                                     "mean",
                                     "validation_status",)}),
        ("Métadonnées", {"description": "Ces informations sont protégées.",
                         "fields": ("word_count",
                                    ("creation_date", "creation_user",),
                                    ("modification_date", "modification_user",),)}),
    )
    readonly_fields = ("word_count", "creation_date", "creation_user", "modification_user",
                       "modification_date", "mean",)

    def mean(self, obj):
        return obj.mean
    mean.short_description = "moyenne"


class BetaAdminAccess(BaseAdminAccess):
    """Accès d'administration aux bêtatages"""

    ordering = ("-id",)
    list_display = ("id", "__str__", "stage",)


admin.site.register(Fiction, FictionAdminAccess)
admin.site.register(Chapter, ChapterAdminAccess)
admin.site.register(Beta, BetaAdminAccess)
