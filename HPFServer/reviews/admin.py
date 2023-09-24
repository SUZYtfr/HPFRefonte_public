from django import forms
from django.contrib import admin
from mptt import admin as mptt_admin

from core.admin import BaseAdminPage
from reviews.models import (
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
        super().save_model(request, obj, form, change)

        text = form.cleaned_data.get("text")
        if not change or (change and text != obj.text):
            obj.versions.create(
                text=text,
                creation_user_id=request.user.id,
            )


class FictionReviewForm(forms.ModelForm):
    text = forms.fields.CharField(
        widget=forms.Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = FictionReview
        fields = ["text"]


class ChapterReviewForm(forms.ModelForm):
    text = forms.fields.CharField(
        widget=forms.Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = ChapterReview
        fields = ["text"]


class CollectionReviewForm(forms.ModelForm):
    text = forms.fields.CharField(
        widget=forms.Textarea({"cols": "100", "rows": "20"}),
        label="Dernière version"
    )

    class Meta:
        model = CollectionReview
        fields = ["text"]


@admin.register(FictionReview)
class FictionReviewAdminAccess(TextFieldMixin, BaseAdminPage, mptt_admin.MPTTModelAdmin):
    """Accès d'administration aux reviews et réponses à reviews de fictions"""

    mptt_indent_field = "__str__"
    list_display = ("id", "__str__", "fiction", "creation_user", "creation_date", "grading", "reply_count")
    fieldsets = [
        (None, {
            "fields": ("fiction", "grading", "parent", "is_draft", "text"),
        }),
    ]
    autocomplete_fields = ["fiction", "parent"]
    search_fields = ["fiction", "parent"]
    form = FictionReviewForm


@admin.register(ChapterReview)
class ChapterReviewAdminAccess(TextFieldMixin, BaseAdminPage, mptt_admin.MPTTModelAdmin):
    """Accès d'administration aux reviews et réponses à reviews de chapitres"""

    mptt_indent_field = "__str__"
    list_display = ("id", "__str__", "chapter", "creation_user", "creation_date", "grading", "reply_count")
    fieldsets = [
        (None, {
            "fields": ("chapter", "grading", "parent", "is_draft", "text"),
        }),
    ]
    autocomplete_fields = ["chapter", "parent"]
    search_fields = ["chapter", "parent"]
    form = ChapterReviewForm


@admin.register(CollectionReview)
class CollectionReviewAdminAccess(TextFieldMixin, BaseAdminPage, mptt_admin.MPTTModelAdmin):
    """Accès d'administration aux reviews et réponses à reviews de séries"""

    mptt_indent_field = "__str__"
    list_display = ("id", "__str__", "collection", "creation_user", "creation_date", "grading", "reply_count")
    fieldsets = [
        (None, {
            "fields": ("collection", "grading", "parent", "is_draft", "text"),
        }),
    ]
    autocomplete_fields = ["collection", "parent"]
    search_fields = ["collection", "parent"]
    form = CollectionReviewForm
