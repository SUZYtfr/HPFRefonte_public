from django import forms
from django.contrib import admin
from django.http import HttpRequest
from django.forms import ModelForm
from django.db import transaction
from ordered_model import admin as ordered_admin

from core.admin import BaseAdminPage
from core.text_functions import count_words
from fictions.models import (
    Collection,
    CollectionItem,
    Fiction,
    Chapter,
    ChapterVersion,
    InvalidationReason,
    Fandom,
)

from typing import Any


class CollectionItemInline(ordered_admin.OrderedTabularInline):
    verbose_name = "élément"
    model = CollectionItem
    fk_name = "parent"
    extra = 0
    min_num = 1
    fields = [
        "id",
        "collection",
        "fiction",
        "chapter",
        "move_up_down_links",
    ]
    readonly_fields = ["move_up_down_links"]
    ordering = ["order"]
    autocomplete_fields = ["collection", "fiction", "chapter"]


@admin.register(Collection)
class CollectionAdminPage(ordered_admin.OrderedInlineModelAdminMixin, BaseAdminPage):
    """Accès d'administration des séries"""

    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "title", "creation_user", "access"]
    list_display_links = ["title"]
    list_filter =  ["access"]
    search_fields = ["title"]
    fieldsets = [
        (None, {
            "fields": ("title", "summary", "access"),
        }),
        ("Caractéristiques", {
            "fields": ("characteristics",),
            "classes": ["collapse"],
        }),
        ("Statistiques", {
            "fields": ("average",),
            "classes": ["collapse"],
        }),
    ]
    inlines = [CollectionItemInline]
    readonly_fields = ["average"]
    autocomplete_fields = ["characteristics"]


@admin.register(Fiction)
class FictionAdminPage(BaseAdminPage):
    """Accès d'administration des fictions"""

    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "title", "creation_user", "last_update_date", "status", "published"]
    list_display_links = ["title"]
    list_filter =  ["status", "last_update_date"]
    search_fields = ["title"]
    fieldsets = [
        (None, {
            "fields": ("title", "storynote", "summary", "status", "featured", "published"),
        }),
        ("Caractéristiques", {
            "fields": ("characteristics", "fandoms"),
            "classes": ["collapse"],
        }),
        ("Statistiques", {
            "fields": ("average", "chapter_count", "word_count", "read_count"),
            "classes": ["collapse"],
        }),
        # ("Autres", {
        #     "fields": ("coauthors",),
        #     "classes": ["collapse"],
        # })
    ]
    # autocomplete_fields = ["coauthors", "characteristics"]
    autocomplete_fields = ["characteristics", "fandoms"]
    readonly_fields = ["read_count", "last_update_date", "published", "average", "word_count", "chapter_count"]

    @admin.display(description="publiée", boolean=True)
    def published(self, fiction: Fiction) -> bool:
        return fiction.is_published


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = [
            "title",
            "start_note",
            "end_note",
            "text",
            "make_published",
        ]

    title = forms.fields.CharField(label="titre")
    start_note = forms.fields.CharField(label="start_note", required=False)
    end_note = forms.fields.CharField(label="end_note", required=False)
    text = forms.fields.CharField(
        widget=forms.Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version",
    )
    make_published = forms.fields.BooleanField(label="publier cette version", required=False)


@admin.register(Chapter)
class ChapterAdminPage(BaseAdminPage):
    """Page d'administration des chapitres"""

    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "title", "creation_user", "creation_date", "is_published"]
    list_display_links = ["title"]
    list_filter = ["creation_date"]
    search_fields = ["title"]
    fieldsets = [
        (None, {
            "fields": ("fiction", "title", "start_note", "end_note", "is_published", "read_count", "text", "trigger_warnings", "make_published"),
        }),
        ("Statistiques", {
            "fields": ("average", "word_count"),
            "classes": ["collapse"],
        }),
    ]
    readonly_fields = ["word_count", "average", "is_published"]
    autocomplete_fields = ["fiction"]
    form = ChapterForm

    # def display_is_published(self, request: HttpRequest, chapter: Chapter) -> bool:
    #     return chapter.is_published

    # @admin.display(description="title")
    # def display_title(self, chapter: Chapter) -> str | None:
    #     if title := chapter.title:
    #         return title
    #     elif last_version_title := getattr(chapter.last_version, "title", None):
    #         return f"{last_version_title} (non publié)"
    #     else:
    #         return "Sans titre"  # ne devrait jamais arriver

    def get_readonly_fields(self, request: HttpRequest, chapter: Chapter | None = None) -> list[str] | tuple[str, Any]:
        readonly_fields = super().get_readonly_fields(request, chapter)
        if chapter:
            return readonly_fields + ["fiction"]
        else:
            return readonly_fields

    def get_form(self, request: HttpRequest, chapter: Chapter, change: bool, **kwargs) -> ModelForm:
        form = super().get_form(request, chapter, change, **kwargs)
        if change:
            form.base_fields["title"].initial = chapter.title
            form.base_fields["text"].initial = chapter.text
            form.base_fields["start_note"].initial = chapter.start_note
            form.base_fields["end_note"].initial = chapter.end_note
        return form

    @transaction.atomic
    def save_model(self, request: HttpRequest, chapter: Chapter, form: ModelForm, change: bool) -> None:
        title = form.cleaned_data.pop("title")
        text = form.cleaned_data.pop("text")
        start_note = form.cleaned_data.pop("start_note")
        end_note = form.cleaned_data.pop("end_note")
        make_published = form.cleaned_data.pop("make_published")

        super().save_model(request, chapter, form, change)

        if any([
            title != chapter.title,
            text != chapter.text,
            start_note != chapter.start_note,
            end_note != chapter.end_note,
        ]):
            version = ChapterVersion.objects.create(
                chapter=chapter,
                title=title,
                text=text,
                start_note=start_note,
                end_note=end_note,
                # invalidation=chapter.invalidation,
                word_count=count_words(text),
                creation_user=request.user,
            )
            if make_published:
                chapter.published_version = version
                chapter.save()

@admin.register(ChapterVersion)
class ChapterVersionAdminPage(admin.ModelAdmin):
    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "chapter", "creation_user", "creation_date", "word_count", "display_status"]
    list_display_links = ["chapter"]
    search_fields = ["chapter"]
    readonly_fields = [
        "creation_date",
        "creation_user",
        "chapter",
        "word_count",
        "text",
        "display_status",
        "display_invalidation_reasons",
    ]
    fieldsets = [
        (None, {
            "fields": ["chapter", "text", "word_count", "submission_date"],
        }),
        ("Invalidation", {
            "fields": ["public_comment", "private_comment", "invalidation_date", "invalidation_user", "display_invalidation_reasons", "to_be_discussed"],
        }),
        ("Métadonnées", {
            "fields": [
                ("creation_user", "creation_date"),
            ],
            "classes": ["collapse"],
        }),
    ]

    @admin.display(description="raisons d'invalidation")
    def display_invalidation_reasons(self, chapter_version: ChapterVersion) -> str:
        return ", ".join(chapter_version.invalidation_reasons.values_list("reason", flat=True))

    @admin.display(description="status")
    def display_status(self, chapter_version: ChapterVersion) -> str:
        return chapter_version.validation_status.label

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


@admin.register(InvalidationReason)
class InvalidationReasonAdmin(admin.ModelAdmin):
    pass


@admin.register(Fandom)
class FandomAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "display_fiction_count"]
    search_fields = ["name"]

    @admin.display(description="fictions")
    def display_fiction_count(self, fandom: "Fandom") -> int:
        return fandom.fictions.count()
