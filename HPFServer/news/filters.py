from django_filters import rest_framework as filters

from .models import NewsArticle

class NewsArticleFilterSet(filters.FilterSet):
    searchAuthor = filters.CharFilter(
        field_name="creation_user__username",
        lookup_expr="icontains",
        label="Écrite par",
    )
    searchTerm = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label="Le titre contient",
    )
    fromDate = filters.DateTimeFilter(
        field_name="post_date",
        lookup_expr="gt",
        label="Publiée après le",
    )
    toDate = filters.DateTimeFilter(
        field_name="post_date",
        lookup_expr="lt",
        label="Publiée avant le",
    )

    class Meta:
        model = NewsArticle
        fields = [
            "searchAuthor",
            "searchTerm",
            "fromDate",
            "toDate",
        ]
