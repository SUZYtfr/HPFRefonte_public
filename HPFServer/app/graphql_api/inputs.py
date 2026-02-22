import strawberry_django
from strawberry import auto

from news.models import NewsComment
from fictions.models import Fiction, Chapter, ChapterVersion
from reviews.models import BaseReview, ChapterReview, FictionReview


### NEWS
@strawberry_django.input(model=NewsComment)
class NewsCommentInput:
    text: auto


### FICTIONS
@strawberry_django.input(model=Fiction)
class FictionInput:
    title: auto


@strawberry_django.input(model=Chapter)
class ChapterInput:
    title: str
    text: str


### REVIEWS
@strawberry_django.input(model=BaseReview)
class ReviewInput:
    text: str
    grading: int | None


@strawberry_django.input(model=ChapterReview)
class ChapterReviewInput:
    text: str
    grading: int | None


@strawberry_django.input(model=FictionReview)
class FictionReviewInput:
    text: str
    grading: int | None


@strawberry_django.input(model=ChapterVersion)  # seulement les champs concernés
class InvalidationInput:
    public_comment: auto
    private_comment: auto
    invalidation_reasons: list[int]
    to_be_discussed: auto

