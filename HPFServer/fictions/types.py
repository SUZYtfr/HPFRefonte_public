from graphene import List, String, Int, ObjectType
from graphene_django import DjangoObjectType, DjangoListField
from fictions.models import Collection, Chapter, Fiction

from users.types import UserType


class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
            "summary",
        ]


class ChapterType(DjangoObjectType):
    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "startnote",
            "endnote",
            "text",
        ]

    text = String()



class FictionType(DjangoObjectType):
    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
            "summary",
            "storynote",
            "last_update_date",
            "creation_date",
            "status",
            "word_count",
            "read_count",
            "chapter_count",
            "review_count",
            "average",
            "chapters",
            "characteristics",
            "authors",
        ]

    authors = DjangoListField(UserType)
    word_count = Int()
    read_count = Int()
    chapter_count = Int()
    review_count = Int()
    average = Int()


class PaginatedFictionType(ObjectType):
    results = DjangoListField(FictionType)
    # pageSize = Int()
    # totalPages = Int()
    # currentPage = Int()
    count = Int()
    current = Int()