from django.contrib import admin
from .models import ChapterTextVersion, ReviewTextVersion


class TextAdminAccess(admin.ModelAdmin):
    """Accès d'administration aux historiques de textes"""

    list_display = ("id", "__str__", "creation_user")
    fields = ("text",)
    readonly_fields = ("creation_user", "__str__", "text",)


admin.site.register(ChapterTextVersion, TextAdminAccess)
admin.site.register(ReviewTextVersion, TextAdminAccess)
