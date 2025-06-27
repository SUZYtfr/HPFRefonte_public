from django.db import models
from django_filters import rest_framework as filters
from django.contrib.postgres.search import SearchVector

from characteristics.models import Characteristic
from fictions.models import Fiction, Chapter
from fictions.enums import FictionStatus, ChapterValidationStage


class FictionFilterSet(filters.FilterSet):
    class Meta:
        model = Fiction
        fields = [
            "search_author",
            # "coauthor",
            # "authors"
            "search_term",
            "summary",
            "word_count",
            "status",
            "included_tags",
            "excluded_tags",
            "featured",
            "search_author_id",
        ]


    search_author = filters.CharFilter(
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
    search_term = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label="Le titre contient",
    )
    summary = filters.CharFilter(
        lookup_expr="icontains",
        label="Le résumé contient",
    )
    word_count = filters.RangeFilter(
        field_name="_word_count",
        label="Plage de compte de mots",
    )

    included_tags = filters.ModelMultipleChoiceFilter(
        field_name="characteristics",
        label="Avec les caractéristiques",
        conjoined=True,
        queryset=Characteristic.objects.allowed(),
    )
    excluded_tags = filters.ModelMultipleChoiceFilter(
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
    sort_by = filters.CharFilter(
        method="sort_by",
        label="trier selon",
    )
    from_date = filters.DateTimeFilter(
        field_name="creation_date",
        lookup_expr="gt",
        label="Écrite après le",
    )
    to_date = filters.DateTimeFilter(
        field_name="creation_date",
        lookup_expr="lt",
        label="Écrite avant le",
    )
    search_author_id = filters.NumberFilter(
        field_name="creation_user",
        label="ID auteur",
    )

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
            "most_rating": "-average",
            "less_rating": "average",
        }
        return queryset.order_by(corres.get(value, "-creation_date"))


class ChapterFilterSet(filters.FilterSet):
    class Meta:
        model = Chapter
        fields = [
            "validation_status",
            "search",
        ]

    validation_status = filters.MultipleChoiceFilter(
        choices=ChapterValidationStage.choices,
    )
    search = filters.CharFilter(
        method="search_multi",
    )
    moderation_date = filters.DateTimeFromToRangeFilter(

    )

    def search_multi(self, queryset, name, value):
        queryset = queryset.annotate(
            search=SearchVector(
                "start_note",
                "end_note",
                "creation_user__username",
                "title",
                "fiction_title"
            ),
        ).filter(
            search__contains=value,
        )
        return queryset

    # moderation__date
    # chapter__last_version__moderation_date__between=value,value