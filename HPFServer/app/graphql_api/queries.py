from django.db.models import QuerySet, Prefetch
import strawberry
import strawberry_django
from strawberry import Info
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsStaff, IsAuthenticated
from strawberry_django.auth.utils import get_current_user
from fictions.models import Fiction, Chapter, ChapterVersion, Fandom
from news.models import NewsArticle, NewsStatus
from reviews.models import ChapterReview, FictionReview
from app.graphql_api.types import (
    FandomType,
    FictionType,
    ChapterType,
    ChapterVersionType,
    CollectionType,
    NewsArticleType,
    UserType,
    ThemeType,
    CharacteristicType,
    CharacteristicTypeType,
    TriggerWarningType,
    ChapterReviewType,
    FictionReviewType,
)


# PUBLIQUE

def resolve_fandom_by_slug(slug: str) -> Fandom:
    return Fandom.objects.get(slug=slug)


def resolve_public_fictions(pk: strawberry.ID | None = None) -> QuerySet[Fiction] | Fiction:
    queryset = Fiction.objects.published().prefetch_related(
        Prefetch("chapters", Chapter.objects.published()),
    ).with_word_counts()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_public_chapters(pk: strawberry.ID | None = None) -> QuerySet[Chapter] | Chapter:
    queryset = Chapter.objects.published()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_public_fiction_reviews() -> QuerySet[FictionReview]:
    return FictionReview.objects.reviews().published()


def resolve_public_chapter_reviews() -> QuerySet[ChapterReview]:
    return ChapterReview.objects.reviews().published()


def resolve_public_news(pk: strawberry.ID | None = None) -> QuerySet[NewsArticle] | NewsArticle:
    queryset = NewsArticle.objects.filter(status=NewsStatus.PUBLISHED)
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset

# PRIVÉ

def resolve_private_fictions(info: Info, pk: strawberry.ID | None = None) -> QuerySet[Fiction] | Fiction:
    current_user = get_current_user(info)
    queryset = current_user.created_fictions.all()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_private_chapters(info: Info, pk: strawberry.ID | None = None) -> QuerySet[Chapter] | Chapter:
    current_user = get_current_user(info)
    queryset = current_user.created_chapters.all()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


# ADMIN

def resolve_admin_chapter_versions() -> QuerySet[ChapterVersion]:
    return ChapterVersion.objects.exclude(submission_date__isnull=True)


@strawberry.type
class Query:
    # publique
    fandom_by_slug: FandomType = strawberry_django.field(resolver=resolve_fandom_by_slug)
    fandoms: list[FandomType] = strawberry_django.field()
    fiction: FictionType = strawberry_django.field(resolver=resolve_public_fictions)
    fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(resolver=resolve_public_fictions)
    chapter: ChapterType = strawberry_django.field(resolver=resolve_public_chapters)
    chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(resolver=resolve_public_chapters)
    collections: OffsetPaginated[CollectionType] = strawberry_django.offset_paginated()
    fiction_reviews: OffsetPaginated[FictionReviewType] = strawberry_django.offset_paginated(resolver=resolve_public_fiction_reviews)
    chapter_reviews: OffsetPaginated[ChapterReviewType] = strawberry_django.offset_paginated(resolver=resolve_public_chapter_reviews)
    news_article: NewsArticleType = strawberry_django.field(resolver=resolve_public_news)
    news_articles: OffsetPaginated[NewsArticleType] = strawberry_django.offset_paginated(resolver=resolve_public_news)
    users: OffsetPaginated[UserType] = strawberry_django.offset_paginated()
    themes: list[ThemeType] = strawberry_django.field()
    characteristic_types: list[CharacteristicTypeType] = strawberry_django.field()
    characteristics: list[CharacteristicType] = strawberry_django.field()
    trigger_warnings: list[TriggerWarningType] = strawberry_django.field()
    # TODO renommer en public_fictions, etc?

    # privé
    account: UserType = strawberry_django.auth.current_user()  # a son propre check d'auth

    private_fiction: FictionType = strawberry_django.field(
        resolver=resolve_private_fictions,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    private_fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(
        resolver=resolve_private_fictions,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    private_chapter: ChapterType = strawberry_django.field(
        resolver=resolve_private_chapters,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    private_chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(
        resolver=resolve_private_chapters,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    # TODO private_fictions, etc? ou accès par account > created_fictions?

    # admin
    admin_fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(
        extensions=[IsStaff(fail_silently=False), IsAuthenticated(fail_silently=False)],
    )
    admin_chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(
        extensions=[IsStaff(fail_silently=False), IsAuthenticated(fail_silently=False)],
    )
    admin_chapter_versions: OffsetPaginated[ChapterVersionType] = strawberry_django.offset_paginated(
        resolver=resolve_admin_chapter_versions,
        extensions=[IsStaff(fail_silently=False), IsAuthenticated(fail_silently=False)],
    )
