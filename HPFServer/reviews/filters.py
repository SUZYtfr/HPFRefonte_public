from django.forms import IntegerField
from django_filters import (
    FilterSet,
    CharFilter,
    ModelChoiceFilter,
    MultipleChoiceFilter,
)
from django.db.models import Q, F, Subquery
from django.contrib.contenttypes.models import ContentType

from users.models import User
from .models import (
    BaseReview,
    CollectionReview,
    FictionReview,
    ChapterReview,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field

class CollectionReviewFilterset(FilterSet):
    class Meta:
        model = CollectionReview
        fields = [
            "content",
        ]

    content = CharFilter(
        label="Recherche partielle dans les titres et pseudonymes.",
        method="filter_content",
    )

    def filter_content(self, queryset, name, value):
        return queryset.filter(
            Q(creation_user__username__contains=value)
            |
            Q(collection__creation_user__username__contains=value)
            |
            Q(collection__title__contains=value)
        )


class FictionReviewFilterset(FilterSet):
    class Meta:
        model = FictionReview
        fields = [
            "content",
        ]

    content = CharFilter(
        label="Recherche partielle dans les titres et pseudonymes.",
        method="filter_content",
    )

    def filter_content(self, queryset, name, value):
        return queryset.filter(
            Q(creation_user__username__contains=value)
            |
            Q(fiction__creation_user__username__contains=value)
            |
            Q(fiction__title__contains=value)
        )


class ChapterReviewFilterset(FilterSet):
    class Meta:
        model = ChapterReview
        fields = [
            "content",
        ]

    content = CharFilter(
        label="Recherche partielle dans les titres et pseudonymes.",
        method="filter_content",
    )

    def filter_content(self, queryset, name, value):
        return queryset.filter(
            Q(creation_user__username__contains=value)
            |
            Q(chapter__creation_user__username__contains=value)
            |
            Q(chapter__title__contains=value)
        )


class AllReviewFilterset(FilterSet):
    class Meta:
        model = BaseReview
        fields = [
            "posted_by",
            "received_by",
            "content",
            "include",
        ]

    content_type_dict = ContentType.objects.get_for_models(CollectionReview, BaseReview, ChapterReview)
    content_type_choices = tuple((int(v.id), str(k.__name__)) for k, v in content_type_dict.items())

    posted_by = ModelChoiceFilter(
        label="Reviews postées par l'utilisateur·ice.",
        queryset=User.objects.all(),
        method="filter_posted_by",
    )
    received_by = ModelChoiceFilter(
        label="Reviews reçues par l'utilisateur·ice.",
        queryset=User.objects.all(),
        method="filter_received_by",
    )
    content = CharFilter(
        label="Recherche partielle dans les titres et pseudonymes.",
        method="filter_content",
    )
    include = MultipleChoiceFilter(
        label="Modèles de reviews inclus dans la recherche.",
        method="include_models",
        choices=content_type_choices,
    )

    @extend_schema_field(OpenApiTypes.INT)
    def filter_posted_by(self, queryset, name, value):
        return queryset.filter(
            creation_user=value,
        )

    @extend_schema_field(OpenApiTypes.INT)
    def filter_received_by(self, queryset, name, value):
        return queryset.filter(
            Q(CollectionReview___collection__creation_user=value)
            |
            Q(FictionReview___fiction__creation_user=value)
            |
            Q(ChapterReview___chapter__creation_user=value)
        )

    def filter_content(self, queryset, name, value):
        return queryset.filter(
            Q(creation_user__username__contains=value)
            |
            Q(CollectionReview___collection__creation_user__username__contains=value)
            |
            Q(FictionReview___fiction__creation_user__username__contains=value)
            |
            Q(ChapterReview___chapter__creation_user__username__contains=value)
            |
            Q(CollectionReview___collection__title__contains=value)
            |
            Q(FictionReview___fiction__title__contains=value)
            |
            Q(ChapterReview___chapter__title__contains=value)
        )

    def include_models(self, queryset, name, value):
        return queryset.filter(polymorphic_ctype__in=value)
