from strawberry import auto, cast
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsStaff

from app.graphql_api.permissions import IsStaffOrOwner
from app.graphql_api.filters import (
    UserFilters,
    NewsArticleFilters,
    FictionFilters,
    ChapterFilters,
    FandomFilters,
    ChapterReviewFilters,
    FictionReviewFilters,
)
from app.graphql_api.orders import (
    NewsArticleOrder,
    FictionOrder,
    ChapterOrder,
    ChapterReviewOrder,
    FictionReviewOrder,
)

from fictions.models import (
    Fandom,
    Fiction,
    Chapter,
    ChapterVersion,
    InvalidationReason,
    Collection,
    CollectionItem,
    ChapterValidationStage,
)
from reviews.models import ChapterReview, FictionReview
from characteristics.models import (
    Characteristic,
    CharacteristicType as CharType,
    TriggerWarning,
)
from users.models import User, UserPreferences, UserProfile, Theme
from news.models import NewsArticle, NewsComment
from images.models import ContentImage

from typing import Optional


### USERS & SITES

@strawberry_django.type(model=UserPreferences, fields="__all__")
class UserPreferencesType:
    user: "UserType"
    theme: Optional[int] = strawberry_django.field(field_name="theme_id")
    # theme: "ThemeType"  # TODO


@strawberry_django.type(model=UserProfile, fields="__all__")
class UserProfileType:
    user: "UserType"
    modification_user: "UserType"
    bio_images: list["ContentImageType"]
    profile_picture: "ContentImageType"


@strawberry_django.type(model=User, exclude=["password"], filters=UserFilters)
class UserType:
    id: int
    username: str
    profile: "UserProfileType"
    preferences: "UserPreferencesType"
    is_watched: auto = strawberry_django.field(extensions=[IsStaff()])


@strawberry_django.type(model=Theme, fields="__all__")
class ThemeType:
    pass


### CHARACTERISTICS

@strawberry_django.type(model=Characteristic, fields="__all__")
class CharacteristicType:
    _order: int
    creation_user: "UserType"
    modification_user: "UserType"
    characteristic_type: "CharacteristicTypeType"
    parent: Optional["CharacteristicType"]
    replace_with: Optional["CharacteristicType"]
    characteristic_type_id: auto


@strawberry_django.type(model=CharType, fields="__all__")
class CharacteristicTypeType:
    characteristics: list["CharacteristicType"]
    creation_user: "UserType"
    modification_user: "UserType"


@strawberry_django.type(model=TriggerWarning, fields="__all__")
class TriggerWarningType:
    creation_user: "UserType"
    modification_user: "UserType"


### FICTIONS

@strawberry_django.type(model=Chapter, fields="__all__", filters=ChapterFilters, order=ChapterOrder)
class ChapterType:
    def resolve_validation_status(self: Chapter) -> ChapterValidationStage:
        return self.last_version.validation_status

    average: auto
    review_count: auto
    _order: int
    order: int = strawberry_django.field(field_name="_order")
    trigger_warnings: list["TriggerWarningType"]
    versions: OffsetPaginated["ChapterVersionType"] = strawberry_django.offset_paginated(
        extensions=[IsStaffOrOwner(owner_field="creation_user")],
    )
    authors: list["UserType"] = strawberry_django.field(select_related="creation_user")
    creation_user: "UserType"
    modification_user: "UserType"
    fiction: "FictionType"


@strawberry_django.type(model=Fiction, fields="__all__", filters=FictionFilters, order=FictionOrder)
class FictionType:
    chapters: OffsetPaginated["ChapterType"] = strawberry_django.offset_paginated()
    characteristics: list["CharacteristicType"]
    is_watched: auto = strawberry_django.field(extensions=[IsStaff()])
    creation_user: "UserType"
    modification_user: "UserType"
    authors: list["UserType"]
    review_count: auto
    word_count: auto
    read_count: auto
    chapter_count: auto
    average: auto
    is_published: auto
    author: "UserType" = strawberry_django.field(field_name="creation_user")
    fandoms: list["FandomType"]
    trigger_warnings: list["TriggerWarningType"] = strawberry_django.field(prefetch_related="chapters__trigger_warnings")


@strawberry_django.type(model=Collection, fields="__all__")
class CollectionType:
    characteristics: list["CharacteristicTypeType"]
    average: auto
    review_count: auto
    collection_items: list["CollectionItemType"]
    creation_user: "UserType"
    modification_user: "UserType"


@strawberry_django.type(model=CollectionItem, fields="__all__")
class CollectionItemType:
    position: auto
    parent: "CollectionType"
    chapter: Optional["ChapterType"]
    fiction: Optional["FictionType"]
    collection: Optional["CollectionType"]


@strawberry_django.type(model=ChapterVersion, fields="__all__")
class ChapterVersionType:
    invalidation_reasons: list["InvalidationReasonType"]  # TODO IsStaffOrOwner?
    invalidation_user: Optional["UserType"]
    private_comment: auto = strawberry_django.field(extensions=[IsStaff()])
    to_be_discussed: auto = strawberry_django.field(extensions=[IsStaff()])
    chapter: "ChapterType"
    creation_user: "UserType"
    validation_status: "ChapterValidationStage"


@strawberry_django.type(
    model=ChapterReview,
    exclude=["parent"],
    filters=ChapterReviewFilters,
    order=ChapterReviewOrder,
)
class ChapterReviewType:
    text: auto

    @strawberry_django.field(select_related="creation_user")
    def authors(self) -> list["UserType"]:
        return [cast(UserType, self.creation_user)]


@strawberry_django.type(
    model=FictionReview,
    exclude=["parent"],
    filters=FictionReviewFilters,
    order=FictionReviewOrder,
)
class FictionReviewType:
    text: auto

    @strawberry_django.field(select_related="creation_user")
    def authors(self) -> list["UserType"]:
        return [cast(UserType, self.creation_user)]


@strawberry_django.type(model=InvalidationReason, fields="__all__")
class InvalidationReasonType:
    pass


@strawberry_django.type(model=Fandom, fields="__all__", filters=FandomFilters)
class FandomType:
    pass


### NEWS

@strawberry_django.type(model=NewsComment, fields="__all__")
class NewsCommentType:
    creation_user: "UserType"
    modification_user: "UserType"
    newsarticle: "NewsArticleType"
    author: "UserType" = strawberry_django.field(field_name="creation_user")
    content: auto = strawberry_django.field(field_name="text")
    post_date: auto = strawberry_django.field(field_name="creation_date")

@strawberry_django.type(
    model=NewsArticle,
    fields="__all__",
    pagination=True,
    filters=NewsArticleFilters,
    order=NewsArticleOrder,
)
class NewsArticleType:
    comments: list["NewsCommentType"]
    authors: list["UserType"]
    content_images: list["ContentImageType"]
    creation_user: "UserType"
    modification_user: "UserType"
    comment_count: auto


### IMAGES

@strawberry_django.type(model=ContentImage, fields="__all__")
class ContentImageType:
    src: str
    creation_user: "UserType"
    modification_user: "UserType"
