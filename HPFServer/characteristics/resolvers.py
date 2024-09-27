from django.db.models import QuerySet
from characteristics.models import Characteristic, CharacteristicType as CharType
from characteristics.types import PaginatedCharacteristicType, PaginatedCharacteristicTypeType

def resolve_characteristics(root, info, page_size: int, page: int) -> QuerySet[Characteristic]:
    # return Characteristic.objects.all()
    return PaginatedCharacteristicType(
        results=Characteristic.objects.all(),
        count=1000,
        current=1,
    )

def resolve_characteristic_types(root, info, page_size: int, page: int) -> QuerySet[CharType]:
    return PaginatedCharacteristicTypeType(
        results=CharType.objects.all(),
        count=1000,
        current=1,
    )
