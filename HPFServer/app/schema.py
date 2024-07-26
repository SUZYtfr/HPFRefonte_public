from graphene import ObjectType, Schema, Field, List, String, Int, Argument
from graphene.relay import Node
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from users.models import User, UserProfile
from fictions.models import Fiction, Chapter, Collection
from characteristics.models import Characteristic, CharacteristicType
from news.models import NewsArticle

from math import ceil


class ProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        fields = [
            "realname",
            "bio",
        ]


class StatsType(ObjectType):
    fiction_count = Int()
    chapter_count = Int()
    word_count = Int()
    collection_count = Int()
    challenges = Int()
    review_count = Int()
    favorites_fanfictions = Int()
    favorites_series = Int()
    favorites_author = Int()


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]
        interfaces = [Node]


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            # "status",
            "first_seen",
        ]

    profile = Field(ProfileType)
    stats = Field(StatsType)
    
    @classmethod
    def resolve_stats(root, instance: User, info):
        return dict(
            fiction_count=instance.fiction_count,
            chapter_count=instance.chapter_count,
            word_count=instance.word_count,
            collection_count=instance.collection_count,
            challenges=0,
            review_count=0,
            favorites_fanfictions=0,
            favorites_series=0,
            favorites_author=0,
        )

    @classmethod
    def resolve_profile(root, instance: User, info):
        return instance.profile


class NewsType(DjangoObjectType):
    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "content",
            "post_date",
            "creation_user",
            "authors",
        ]

class CharacteristicTypeType(DjangoObjectType):
    class Meta:
        model = CharacteristicType
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
            "characteristic_type",
            "characteristic_type_id",
        ]
    
    characteristic_type_id = Int()
    

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

    authors = List(UserType)
    word_count = Int()
    read_count = Int()
    chapter_count = Int()
    review_count = Int()
    average = Int()


class PaginatedFictionType(ObjectType):
    results = List(FictionType)
    # pageSize = Int()
    # totalPages = Int()
    # currentPage = Int()
    count = Int()
    current = Int()


class PaginatedNewsType(ObjectType):
    results = List(NewsType)
    count = Int()
    current = Int()


class Query(ObjectType):
    fictions = List(FictionType)
    paginated_fictions = Field(
        PaginatedFictionType,
        pageSize=Argument(Int, default_value=10),
        page=Argument(Int, default_value=0),
    )
    news = List(NewsType)
    paginated_news = Field(PaginatedNewsType)
    users = DjangoConnectionField(UserNode)
    user = Field(
        UserType,
        id=Argument(Int, required=True),
    )

    def resolve_fictions(root, info):
        return Fiction.objects.published()

    def resolve_paginated_fictions(root, info, pageSize: int, page: int):
        page_size = pageSize
        offset = page_size * page
        initial_fictions = Fiction.objects.published()
        current_page = ceil(offset / page_size) + 1
        total_pages = ceil(initial_fictions.count() / page_size)
        subset_fictions = initial_fictions[offset:offset+page_size]

        return dict(
            results=subset_fictions,
            count=initial_fictions.count(),
            current=current_page,
            # pageSize=page_size,
            # currentPage=current_page,
            # totalPages=total_pages,
        )

    def resolve_paginated_news(root, info):
        news = NewsArticle.objects.all()
        return dict(
            results=news,
            count=112,
            current=1,
        )

    def resolve_users(root, info):
        return User.objects.all()

    def resolve_user(root, info, id: int):
        return User.objects.get(pk=id)


schema = Schema(query=Query, auto_camelcase=False)
