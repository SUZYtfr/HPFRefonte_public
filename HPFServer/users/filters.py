from django.db.models import CharField
from django_filters import rest_framework as filters

from users.models import User


class UserFilterSet(filters.FilterSet):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "id",
            "status",
            "first_seen",
        ]

    username = filters.CharFilter(lookup_expr="icontains")
    email = filters.CharFilter(lookup_expr="icontains")
    status = filters.NumberFilter(method="filter_status")
    first_seen = filters.DateTimeFilter(lookup_expr="date")

    def filter_status(self, queryset, name, value):
        if value == 1:
            return queryset.filter(
                is_active=False,
                username__isnull=False,
            )
        elif value == 2:
            return queryset.filter(
                is_active=True,
                is_staff=False,
                is_superuser=False,
                username__isnull=False,
            )
        elif value == 3:
            return queryset.filter(
                is_active=True,
                is_staff=True,
                is_superuser=False,
            )
        elif value == 4:
            return queryset.filter(
                is_active=True,
                is_superuser=True
            )
        elif value == 5:
            return queryset.filter(
                is_active=False,
                username__isnull=True,
            )
        else:
            return queryset
