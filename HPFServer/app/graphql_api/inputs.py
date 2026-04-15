import strawberry
import strawberry_django
from strawberry import auto, ID
from strawberry_django import ListInput

from news.models import NewsComment
from fictions.models import Fiction, Chapter, ChapterVersion, Collection
from reviews.models import BaseReview, ChapterReview, FictionReview, CollectionReview
from users.models import UserPreferences


### COMPTE
@strawberry_django.input(model=UserPreferences)
class UserPreferencesInput:
    display_content: auto
    theme: int | None = None
    theme_overriden_at: auto
    color_scheme: auto
    color_scheme_in_reader: auto
    show_animations: auto
    show_profile_pictures: auto
    font: auto
    font_size: auto
    line_spacing: auto
    letter_spacing: auto
    paragraph_spacing: auto
    redirect_to_summary: auto
    show_trigger_warnings: auto
    show_review_editor: auto
    email_for_review: auto
    email_for_reply: auto
    email_for_news: auto
    email_for_favorite: auto
    email_for_favorite_activity: auto
    email_for_chapter_status: auto
    member_review_policy: auto
    anonymous_review_policy: auto
    result_order: auto


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


@strawberry_django.input(model=Collection)
class CollectionInput:
    title: auto
    summary: auto
    access: auto
    fandoms: ListInput[ID] | None
    characteristics: ListInput[ID] | None


@strawberry.input(one_of=True)
class CollectionItemInput:
    fiction_id: strawberry.Maybe[strawberry.ID]
    chapter_id: strawberry.Maybe[strawberry.ID]
    collection_id: strawberry.Maybe[strawberry.ID]


### REVIEWS
@strawberry_django.input(model=BaseReview)
class ReviewInput:
    text: str
    grading: int | None = None


@strawberry_django.input(model=ChapterReview)
class ChapterReviewInput:
    text: str
    grading: int | None = None


@strawberry_django.input(model=FictionReview)
class FictionReviewInput:
    text: str
    grading: int | None = None


@strawberry_django.input(model=CollectionReview)
class CollectionReviewInput:
    text: str
    grading: int | None = None


@strawberry_django.input(model=ChapterVersion)  # seulement les champs concernés
class InvalidationInput:
    public_comment: auto
    private_comment: auto
    invalidation_reasons: list[int]
    to_be_discussed: auto
