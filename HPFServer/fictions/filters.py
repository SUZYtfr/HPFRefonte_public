from django.db import models
from django_filters import rest_framework as filters

from characteristics.models import Characteristic
from .models import Fiction
from .enums import FictionStatus


class FictionFilterSet(filters.FilterSet):
    author = filters.CharFilter(
        field_name="creation_user__username",
        lookup_expr="icontains",
        label="Écrite par",
    )
    # FIXME - pas un multi-charfield...
    # coauthor = filters.MultipleChoiceFilter(
    #     field_name="coauthors__username",
    #     lookup_expr="icontains",
    #     conjoined=True,
    #     label="co-écrite par",
    # )
    # TODO - combiner creation_user avec coauthors quand on pourra régler ci-dessus
    # authors = filters.CharFilter(
    #     method="filter_authors",
    #     label="écrite par",
    # )
    title = filters.CharFilter(
        lookup_expr="icontains",
        label="Le titre contient",
    )
    summary = filters.CharFilter(
        lookup_expr="icontains",
        label="Le résumé contient",
    )
    # maxWords = filters.NumberFilter(
    #     field_name="word_count",
    #     lookup_expr="lte",
    #     label="Minimum de mots",
    # )
    # minWords = filters.NumberFilter(
    #     field_name="word_count",
    #     lookup_expr="gte",
    #     label="maximum de mots",
    # )
    maxWords = filters.NumberFilter(
        method="filter_max_words",
        label="maximum de mots",
    )
    minWords = filters.NumberFilter(
        method="filter_min_words",
        label="minimum de mots",
    )

    includedTags = filters.ModelMultipleChoiceFilter(
        field_name="characteristics",
        label="Avec les caractéristiques",
        conjoined=True,
        queryset=Characteristic.objects.allowed(),
    )
    excludedTags = filters.ModelMultipleChoiceFilter(
        field_name="characteristics",
        label="Sans les caractéristiques",
        conjoined=False,
        queryset=Characteristic.objects.allowed(),
        exclude=True,
    )
    finished = filters.BooleanFilter(
        method="filter_finished",
        label="terminée",
    )
    sortBy = filters.CharFilter(
        method="sort_by",
        label="trier selon",
    )
    fromDate = filters.DateTimeFilter(
        field_name="creation_date",
        lookup_expr="gt",
        label="Écrite après le",
    )
    toDate = filters.DateTimeFilter(
        field_name="creation_date",
        lookup_expr="lt",
        label="Écrite avant le",
    )
    searchAuthorId = filters.NumberFilter(
        field_name="creation_user",
        label="ID auteur",
    )


    class Meta:
        model = Fiction
        fields = [
            "author",
            # "coauthor",
            # "authors"
            "title",
            "summary",
            "minWords",
            "maxWords",
            "status",
            "includedTags",
            "excludedTags",
            "featured",
            "searchAuthorId",
        ]

    def filter_finished(self, queryset, name, value):
        if value == True:
            return queryset.filter(status=FictionStatus.COMPLETED)
        elif value == False:
            return queryset.exclude(status=FictionStatus.COMPLETED)
        return queryset

    def filter_authors(self, queryset, name, value):
        return queryset.filter(
            models.Q(creation_user__username__icontains=value) |
            models.Q(coauthors__username__icontains=value)
        )

    def sort_by(self, queryset, name, value):
        corres = {
            "alpha": "title",
            "most_recent": "-creation_date",
            "less_recent": "creation_date",
            "most_reviews": "-review_count",
            "less_reviews": "review_count",
            "most_rating": "-mean",
            "less_rating": "mean",
        }
        return queryset.order_by(corres.get(value, "-creation_date"))


    def filter_min_words(self, queryset, name, value):
        return queryset.word_counts().filter(annotated_word_count__gte=value)

    def filter_max_words(self, queryset, name, value):
        return queryset.word_counts().filter(annotated_word_count__lte=value)

DjangoFilterBackend = filters.DjangoFilterBackend
