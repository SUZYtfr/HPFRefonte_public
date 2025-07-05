import strawberry_django
from strawberry import auto

from app.graphql_api.types import ChapterVersion

from news.models import NewsComment
from fictions.models import Fiction, Chapter, ChapterVersion


### NEWS
@strawberry_django.input(model=NewsComment)
class NewsCommentInput:
    text: auto


### FICTIONS
@strawberry_django.input(Fiction)
class FictionInput:
    title: auto


@strawberry_django.input(Chapter)
class ChapterInput:
    title: str
    text: str


@strawberry_django.input(model=ChapterVersion)  # seulement les champs concernés
class InvalidationInput:
    public_comment: auto
    private_comment: auto
    invalidation_reasons: list[int]
    to_be_discussed: auto

