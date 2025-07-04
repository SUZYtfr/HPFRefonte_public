from strawberry import auto
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsStaff

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

# Types

@strawberry_django.type(model=UserPreferences, fields="__all__")
class UserPreferencesType:
    pass


@strawberry_django.type(model=UserProfile, fields="__all__")
class UserProfileType:
    pass


@strawberry_django.type(model=User, exclude=["password"])
class UserType:
    profile: "UserProfileType"
    preferences: "UserPreferencesType"
    is_watched: auto = strawberry_django.field(extensions=[IsStaff()])


@strawberry_django.type(model=Theme, fields="__all__")
class ThemeType:
    pass


### CHARACTERISTICS

# Types

@strawberry_django.type(model=Characteristic, fields="__all__")
class CharacteristicType:
    parent_id: auto
    _order: int


@strawberry_django.type(model=CharType, fields="__all__")
class CharacteristicTypeType:
    characteristics: list["CharacteristicType"]


### FICTIONS

# Types

@strawberry_django.type(model=Chapter, fields="__all__")
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
    versions: OffsetPaginated["ChapterVersionType"] = strawberry_django.offset_paginated(extensions=[IsStaff()])
    authors: list["UserType"] = strawberry_django.field(select_related="creation_user")


@strawberry_django.type(model=Fiction, fields="__all__")
class FictionType:
    chapters: list["ChapterType"]
    characteristics: list["CharacteristicType"]


@strawberry_django.type(model=Collection, fields="__all__")
class CollectionType:
    characteristics: list["CharacteristicTypeType"]
    average: auto
    review_count: auto
    collection_items: list["CollectionItemType"]


@strawberry_django.type(model=CollectionItem, fields="__all__")
class CollectionItemType:
    position: auto
    parent: "CollectionType"
    chapter: Optional["ChapterType"]
    fiction: Optional["FictionType"]
    collection: Optional["CollectionType"]


@strawberry_django.type(model=ChapterVersion, fields="__all__")
class ChapterVersionType:
    invalidation_reasons: list["InvalidationReasonType"]


@strawberry_django.type(model=InvalidationReason, fields="__all__")
class InvalidationReasonType:
    pass


### NEWS

# Ordonnations

@strawberry_django.order_type(model=NewsArticle)
class NewsArticleOrder:
    post_date: auto


# Filtres

@strawberry_django.filter_type(model=NewsArticle, lookups=True)
class NewsArticleFilters:
    title: auto
    post_date: auto


# Types

@strawberry_django.type(model=NewsComment, fields="__all__")
class NewsCommentType:
    pass


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


### IMAGES

# Types
@strawberry_django.type(model=ContentImage, fields="__all__")
class ContentImageType:
    src: str
