import strawberry_django
from strawberry import auto, ID
from strawberry_django import ListInput

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
    summary: auto
    storynote: auto
    status: auto
    rating: auto
    fandoms: ListInput[ID] | None
    characteristics: ListInput[ID] | None


@strawberry_django.input(model=Chapter)
class ChapterInput:
    title: str
    text: str
    start_note: str
    end_note: str
    is_draft: bool | None
    trigger_warnings: ListInput[ID] | None


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

