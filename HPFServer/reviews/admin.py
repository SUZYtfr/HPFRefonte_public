from django.forms import (
    ModelForm,
    Textarea,
)
from django.forms.fields import CharField
from django.contrib.admin import ModelAdmin, register
from mptt.admin import MPTTModelAdmin

from core.admin import BaseAdminPage
from .models import (
    BaseReview,
    BaseReviewTextVersion,
    FictionReview,
    ChapterReview,
    CollectionReview,
)


class TextFieldMixin:
    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if change:
            form.base_fields["text"].initial = obj.text
        return form

    def save_model(self, request, obj, form, change):
        text = form.cleaned_data["text"]
        obj.text = text
        super().save_model(request, obj, form, change)


class FictionReviewForm(ModelForm):
    text = CharField(
        widget=Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = FictionReview
        fields = ["text"]


class ChapterReviewForm(ModelForm):
    text = CharField(
        widget=Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = ChapterReview
        fields = ["text"]


class CollectionReviewForm(ModelForm):
    text = CharField(
        widget=Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = CollectionReview
        fields = ["text"]


class ReviewReplyForm(ModelForm):
    text = CharField(
        widget=Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = BaseReview
        fields = ["text"]


@register(FictionReview)
class FictionReviewAdminAccess(TextFieldMixin, BaseAdminPage, MPTTModelAdmin):
    """Accès d'administration aux reviews de fictions"""

    ordering = ["-id"]
    mptt_indent_field = "__str__"
    list_display = ("id", "__str__", "fiction", "creation_user", "creation_date", "grading", "reply_count")
    fieldsets = [
        (None, {
            "fields": ("fiction", "grading", "is_draft", "is_archived", "text"),
        }),
    ]
    autocomplete_fields = ["fiction"]
    search_fields = ["fiction"]
    form = FictionReviewForm


@register(ChapterReview)
class ChapterReviewAdminAccess(TextFieldMixin, BaseAdminPage, MPTTModelAdmin):
    """Accès d'administration aux reviews de chapitres"""

    ordering = ["-id"]
    mptt_indent_field = "__str__"
    list_display = ("id", "__str__", "chapter", "creation_user", "creation_date", "grading", "reply_count")
    fieldsets = [
        (None, {
            "fields": ("chapter", "grading", "is_draft", "is_archived", "text"),
        }),
    ]
    autocomplete_fields = ["chapter"]
    search_fields = ["chapter"]
    form = ChapterReviewForm


@register(CollectionReview)
class CollectionReviewAdminAccess(TextFieldMixin, BaseAdminPage, MPTTModelAdmin):
    """Accès d'administration aux reviews de séries"""

    ordering = ["-id"]
    mptt_indent_field = "__str__"
    list_display = ("id", "__str__", "collection", "creation_user", "creation_date", "grading", "reply_count")
    fieldsets = [
        (None, {
            "fields": ("collection", "grading", "is_draft", "is_archived", "text"),
        }),
    ]
    autocomplete_fields = ["collection"]
    search_fields = ["collection"]
    form = CollectionReviewForm


@register(BaseReview)
class ReviewReplyAdminAccess(TextFieldMixin, BaseAdminPage, MPTTModelAdmin):
    """Accès d'administration aux réponses à reviews"""

    mptt_indent_field = "__str__"
    list_display = ("id", "__str__", "creation_user", "creation_date")
    fieldsets = [
        (None, {
            "fields": ("parent", "is_draft", "is_archived", "text"),
        }),
    ]
    autocomplete_fields = ["parent"]
    search_fields = ["parent"]
    form = ReviewReplyForm

    def has_change_permission(self, request, obj=None, *args, **kwargs):
        if obj and obj.level > 0:
            return True
        return False

    def has_delete_permission(self, request, obj=None, *args, **kwargs):
        if obj and obj.level > 0:
            return True
        return False


@register(BaseReviewTextVersion)
class BaseReviewTextVersionAdminPage(ModelAdmin):
    ordering = ["-id"]
    list_per_page = 20
    list_display = ["id", "base_review", "creation_user", "creation_date"]
    list_display_links = ["base_review"]
    search_fields = ["base_review"]
    fieldsets = [
        (None, {
            "fields": ["base_review", "text"],
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
