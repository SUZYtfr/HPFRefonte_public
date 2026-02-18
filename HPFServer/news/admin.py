from django.contrib import admin
from django.http import HttpRequest
from django.forms import ModelForm

from core.admin import BaseAdminPage
from news.models import NewsArticle, NewsComment

from typing import Any


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

    def save_model(self, request: HttpRequest, news_article: NewsArticle, form: ModelForm, change: bool) -> None:
        super().save_model(request, news_article, form, change)

        if not change:
            news_article.authors.add(request.user)


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

    def get_readonly_fields(self, request: HttpRequest, news_comment: NewsComment | None = None) -> list[str] | tuple[str, Any]:
        readonly_fields = super().get_readonly_fields(request, news_comment)
        if news_comment:
            return readonly_fields + ["newsarticle"]
        else:
            return readonly_fields
