from strawberry import auto
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsStaff

from app.graphql_api.permissions import IsStaffOrOwner
from app.graphql_api.filters import (
    UserFilters,
    NewsArticleFilters,
    FictionFilters,
    ChapterFilters,
)
from app.graphql_api.orders import NewsArticleOrder, FictionOrder, ChapterOrder

from fictions.models import (
    Fiction,
    Chapter,
    ChapterVersion,
    InvalidationReason,
    Collection,
    CollectionItem,
)
from characteristics.models import Characteristic, CharacteristicType as CharType
from users.models import User, UserPreferences, UserProfile, Theme
from news.models import NewsArticle, NewsComment
from images.models import ContentImage

from typing import Optional


### USERS & SITES

@strawberry_django.type(model=UserPreferences, fields="__all__")
class UserPreferencesType:
    user: "UserType"
    theme: "ThemeType"


@strawberry_django.type(model=UserProfile, fields="__all__")
class UserProfileType:
    user: "UserType"
    modification_user: "UserType"


@strawberry_django.type(model=User, exclude=["password"], filters=UserFilters)
class UserType:
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


@strawberry_django.type(model=CharType, fields="__all__")
class CharacteristicTypeType:
    characteristics: list["CharacteristicType"]
    creation_user: "UserType"
    modification_user: "UserType"


### FICTIONS

@strawberry_django.type(model=Chapter, fields="__all__", filters=ChapterFilters, order=ChapterOrder)
class ChapterType:
    is_published: auto = strawberry_django.field(select_related="published_version")
    title: auto = strawberry_django.field(select_related="published_version")
    text: auto = strawberry_django.field(select_related="published_version")
    text_images: list["ContentImageType"] | None = strawberry_django.field(select_related="published_version")
    start_note: auto = strawberry_django.field(select_related="published_version")
    end_note: auto = strawberry_django.field(select_related="published_version")
    word_count: auto = strawberry_django.field(select_related="published_version")
    average: auto
    review_count: auto
    _order: int
    trigger_warnings: list["CharacteristicType"]
    versions: OffsetPaginated["ChapterVersionType"] = strawberry_django.offset_paginated(
        extensions=[IsStaffOrOwner(owner_field="creation_user")],
    )
    authors: list["UserType"] = strawberry_django.field(select_related="creation_user")
    creation_user: "UserType"
    modification_user: "UserType"
    fiction: "FictionType"
    published_version: "ChapterVersionType"


@strawberry_django.type(model=Fiction, fields="__all__", filters=FictionFilters, order=FictionOrder)
class FictionType:
    chapters: OffsetPaginated["ChapterType"] = strawberry_django.offset_paginated()
    characteristics: list["CharacteristicType"]
    is_watched: auto = strawberry_django.field(extensions=[IsStaff()])
    creation_user: "UserType"
    modification_user: "UserType"


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


@strawberry_django.type(model=InvalidationReason, fields="__all__")
class InvalidationReasonType:
    pass


### NEWS

@strawberry_django.type(model=NewsComment, fields="__all__")
class NewsCommentType:
    creation_user: "UserType"
    modification_user: "UserType"
    newsarticle: "NewsArticleType"


@strawberry_django.type(
    model=NewsArticle,
    fields="__all__",
    pagination=True,
    filters=NewsArticleFilters,
    ordering=NewsArticleOrder,
)
class NewsArticleType:
    comments: list["NewsCommentType"]
    authors: list["UserType"]
    content_images: list["ContentImageType"]
    creation_user: "UserType"
    modification_user: "UserType"


### IMAGES

@strawberry_django.type(model=ContentImage, fields="__all__")
class ContentImageType:
    src: str
    creation_user: "UserType"
    modification_user: "UserType"


__all__ = [
    "UserPreferencesType",
    "UserProfileType",
    "UserType",
    "ThemeType",
    "CharacteristicType",
    "CharacteristicTypeType",
    "ChapterType",
    "ChapterVersionType",
    "FictionType",
    "CollectionType",
    "CollectionItemType",
    "NewsCommentType",
    "NewsArticleType",
    "ContentImageType",
]
