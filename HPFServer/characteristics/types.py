from graphene import Int
from graphene_django import DjangoObjectType
from characteristics.models import Characteristic, CharacteristicType as CharType


class CharacteristicTypeType(DjangoObjectType):
    class Meta:
        model = CharType
        fields = [
            "id",
            "name",
            "min_limit",
            "max_limit",
        ]


class CharacteristicType(DjangoObjectType):
    class Meta:
        model = Characteristic
        fields = [
            "id",
            "name",
            "description",
            "parent_id",
            "characteristic_type",
            "characteristic_type_id",
        ]
    
    characteristic_type_id = Int()
    parent_id = Int()

from graphene_django import DjangoListField
from graphene import ObjectType
class PaginatedCharacteristicType(ObjectType):
    results = DjangoListField(CharacteristicType)
    # pageSize = Int()
    # totalPages = Int()
    # currentPage = Int()
    count = Int()
    current = Int()


class PaginatedCharacteristicTypeType(ObjectType):
    results = DjangoListField(CharacteristicTypeType)
    # pageSize = Int()
    # totalPages = Int()
    # currentPage = Int()
    count = Int()
    current = Int()
