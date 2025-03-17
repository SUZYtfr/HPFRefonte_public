from django_filters import rest_framework as filters

from news.models import NewsArticle


class NewsArticleFilterSet(filters.FilterSet):    
    class Meta:
        model = NewsArticle
        fields = [
            "search_author",
            "search_term",
            "from_date",
            "to_date",
        ]

    search_author = filters.CharFilter(
        field_name="creation_user__username",
        lookup_expr="icontains",
        label="Écrite par",
    )
    search_term = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        label="Le titre contient",
    )
    from_date = filters.DateTimeFilter(
        field_name="post_date",
        lookup_expr="gt",
        label="Publiée après le",
    )
    to_date = filters.DateTimeFilter(
        field_name="post_date",
        lookup_expr="lt",
        label="Publiée avant le",
    )
