from django.contrib import admin

from core.admin import BaseAdminPage
from .models import NewsArticle, NewsComment


@admin.register(NewsArticle)
class NewsAdminPage(BaseAdminPage):
    """Page d'administration des actualités"""

    ordering = ["-post_date"]
    list_display = ["id", "title", "status", "post_date"]
    list_display_links = ["title"]
    search_fields = ["title"]
    fieldsets = [
        (None, {
            "fields": ("title", "content", "category", "status", "post_date"),
        }),
        ("Autorat", {
            "fields": ("authors", "teams"),
        })
    ]
    autocomplete_fields = ["authors"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change:
            obj.authors.add(request.user)


@admin.register(NewsComment)
class NewsCommentAdminPage(BaseAdminPage):
    """Page d'administration des commentaires d'actualités"""

    ordering = ["-creation_date"]
    list_display = ["id", "__str__", "creation_user", "creation_date"]
    list_display_links = ["__str__"]
    fieldsets = [
        (None, {
            "fields": ("newsarticle", "text"),
        })
    ]
    autocomplete_fields = ["newsarticle"]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ["newsarticle"]
        else:
            return readonly_fields
