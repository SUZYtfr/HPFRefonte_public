from graphene import ObjectType, Int
from graphene_django import DjangoObjectType, DjangoListField
from news.models import NewsArticle, NewsComment


class NewsArticleType(DjangoObjectType):
    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "content",
            "post_date",
            "creation_user",
            "authors",
            "comments",
        ]


class PaginatedNewsArticlesType(ObjectType):
    results = DjangoListField(NewsArticleType)
    count = Int()
    current = Int()


class CommentType(DjangoObjectType):
    class Meta:
        model = NewsComment
        fields = [
            "id",
            "text",
            "creation_user",
            "creation_date",
        ]
