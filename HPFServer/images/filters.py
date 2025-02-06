from django_filters.rest_framework import filters, filterset
from images.models import ContentImage


class PrivateContentImageFilterSet(filterset.FilterSet):
    class Meta:
        model = ContentImage
        fields = [
            "username",
            "explicit_content_type",
            "missing_credits",
        ]

    username = filters.CharFilter(
        field_name="creation_user__username",
        lookup_expr="icontains",
    )
    missing_credits = filters.BooleanFilter(
        method="filter_missing_credits",
    )

    def filter_missing_credits(self, queryset, name, value):
        if value == True:
            queryset = queryset.filter(
                credits_url__isnull=True,
            )
        elif value == False:
            queryset = queryset.filter(
                credits_url__isnull=False,
            )
        return queryset
    