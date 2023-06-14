from django_filters import rest_framework as filters
from .models import Characteristic


class CharacteristicFilterSet(filters.FilterSet):
    parent_id = filters.NumberFilter()

    class Meta:
        model = Characteristic
        fields = [
            "characteristic_type_id",
            "parent_id",
        ]
