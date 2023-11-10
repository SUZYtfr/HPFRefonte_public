from django import forms
from django.contrib import admin
from django.utils import timezone
from ordered_model import admin as ordered_admin

from core.admin import BaseAdminPage
from .models import (
    Collection,
    CollectionItem,
    Fiction,
    Chapter,
    ChapterTextVersion,
)


class CollectionItemForm(forms.ModelForm):
    def clean(self):
        super().clean()

        collection = self.cleaned_data.get("collection")
        fiction = self.cleaned_data.get("fiction")
        chapter = self.cleaned_data.get("chapter")
        items = list(filter(lambda x: x, [collection, fiction, chapter]))
        
        if len(items) < 1:
            raise forms.ValidationError("Un objet est requis pour l'élément de série.")
        elif len(items) > 1:
            raise forms.ValidationError("Un élément de série ne peut pas contenir plus d'un objet.")

        return self.cleaned_data


class CollectionItemInline(ordered_admin.OrderedTabularInline):
    verbose_name = "élément"
    form = CollectionItemForm
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
            "fields": ("characteristics",),
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
    autocomplete_fields = ["characteristics"]
    readonly_fields = ["read_count", "last_update_date", "published", "average", "word_count", "chapter_count"]

    @admin.display(description="publiée", boolean=True)
    def published(self, obj):
        return obj.is_published


class ChapterForm(forms.ModelForm):
    text = forms.fields.CharField(
        widget=forms.Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = Chapter
        fields = ["text"]


@admin.register(Chapter)
class ChapterAdminPage(BaseAdminPage):
    """Page d'administration des chapitres"""

    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "title", "creation_user", "creation_date", "validation_status"]
    list_display_links = ["title"]
    list_filter = ["validation_status", "creation_date"]
    search_fields = ["title"]
    fieldsets = [
        (None, {
            "fields": ("fiction", "title", "startnote", "endnote", "validation_status", "read_count", "text", "trigger_warnings"),
        }),
        ("Statistiques", {
            "fields": ("average", "word_count"),
            "classes": ["collapse"],
        })
    ]
    readonly_fields = ["word_count", "average"]
    autocomplete_fields = ["fiction"]
    form = ChapterForm

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ["fiction"]
        else:
            return readonly_fields

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if change:
            form.base_fields["text"].initial = obj.text
        return form

    def save_model(self, request, obj, form, change):
        text = form.cleaned_data.get("text")
        obj.text = text
        super().save_model(request, obj, form, change)


@admin.register(ChapterTextVersion)
class ChapterTextVersionAdminPage(admin.ModelAdmin):
    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "chapter", "creation_user", "creation_date", "word_count"]
    list_display_links = ["chapter"]
    search_fields = ["chapter"]
    fieldsets = [
        (None, {
            "fields": ["chapter", "text", "word_count"],
        }),
        ("Métadonnées", {
            "fields": [
                ("creation_user", "creation_date"),
            ],
            "classes": ["collapse"]
        })
    ]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
