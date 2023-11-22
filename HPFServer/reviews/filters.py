from django_filters import (
    FilterSet,
    CharFilter,
    NumberFilter,
    MultipleChoiceFilter,
)
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from .models import (
    BaseReview,
    CollectionReview,
    FictionReview,
    ChapterReview,
)


class ReviewFilterset(FilterSet):
    class Meta:
        model = BaseReview
        fields = [
            "creation_user",
            "searchTerm",
            "include_item_types",
            "item_id",
        ]

    searchTerm = CharFilter(
        label="Recherche partielle dans les titres et pseudonymes.",
        method="filter_content",
    )

    # content_type_dict = ContentType.objects.get_for_models(CollectionReview, FictionReview, ChapterReview)
    # content_type_choices = tuple((int(v.id), str(k.__name__)) for k, v in content_type_dict.items())
    content_type_choices = [
        ("ChapterReview", "ChapterReview"),
        ("FictionReview", "FictionReview"),
        ("CollectionReview", "CollectionReview"),
    ]
    include_item_types = MultipleChoiceFilter(
        label="Modèles de reviews inclus dans la recherche.",
        method="include_models",
        choices=content_type_choices,
    )
    item_id = NumberFilter(
        method="filter_item_id",
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
        content_type_dict = ContentType.objects.get_for_models(CollectionReview, FictionReview, ChapterReview)
        ctypes = [v for k, v in content_type_dict.items() if k.__name__ in value]
        return queryset.filter(polymorphic_ctype__in=ctypes)

    def filter_item_id(self, queryset, name, value):
        return queryset.filter(
            Q(CollectionReview___collection_id=value)
            |
            Q(FictionReview___fiction_id=value)
            |
            Q(ChapterReview___chapter_id=value)
        )
