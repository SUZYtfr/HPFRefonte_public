from graphene import ObjectType, Schema, Field, List, String, Int, Argument, Mutation
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphene_django.filter import DjangoFilterConnectionField

from users.types import UserType, UserNode
from users.resolvers import resolve_user, resolve_users
from fictions.types import PaginatedFictionType
from fictions.resolvers import resolve_paginated_fictions
from news.types import NewsArticleType, PaginatedNewsArticlesType, CommentType
from news.resolvers import resolve_paginated_news_articles, resolve_news_article
from news.mutations import PostComment
from characteristics.types import PaginatedCharacteristicType, PaginatedCharacteristicTypeType
from characteristics.resolvers import resolve_characteristic_types, resolve_characteristics


class Query(ObjectType):
    paginated_fictions = Field(
        PaginatedFictionType,
        page_size=Argument(Int, default_value=10),
        page=Argument(Int, default_value=0),
        search_author=String(),
        search_author_id=Int(),
        resolver=resolve_paginated_fictions
    )
    news_article = Field(
        NewsArticleType,
        news_id=Argument(Int, required=True),
        resolver=resolve_news_article,
    )
    paginated_news_articles = Field(
        PaginatedNewsArticlesType,
        page_size=Argument(Int, default_value=10),
        page=Argument(Int, default_value=0),
        resolver=resolve_paginated_news_articles,
    )
    paginated_characteristics = Field(
        PaginatedCharacteristicType,
        page_size=Argument(Int, default_value=1000),
        page=Argument(Int, default_value=0),
        resolver=resolve_characteristics,
    )
    paginated_characteristic_types = Field(
        PaginatedCharacteristicTypeType,
        page_size=Argument(Int, default_value=1000),
        page=Argument(Int, default_value=0),
        resolver=resolve_characteristic_types,
    )
    users = DjangoConnectionField(
        UserNode,
        resolver=resolve_users,
    )
    user = Field(
        UserType,
        user_id=Argument(Int, required=True),
        resolver=resolve_user,
    )
    characteristics = Field(PaginatedCharacteristicType)
    characteristic_types = Field(PaginatedCharacteristicTypeType)


class Mutation(ObjectType):
    post_comment = PostComment.Field()


schema = Schema(query=Query, mutation=Mutation, auto_camelcase=True)
