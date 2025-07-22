import strawberry
import strawberry_django
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsStaff
from fictions.models import Fiction, Chapter, ChapterVersion
from news.models import NewsArticle, NewsStatus
from app.graphql_api.types import *


def resolve_public_fictions():
    return Fiction.objects.published()


def resolve_public_chapters():
    return Chapter.objects.published()


def resolve_public_news():
    return NewsArticle.objects.filter(status=NewsStatus.PUBLISHED)


def resolve_admin_chapter_versions():
    return ChapterVersion.objects.exclude(submission_date__isnull=True)


@strawberry.type
class Query:
    # publique
    fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(resolver=resolve_public_fictions)
    chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(resolver=resolve_public_chapters)
    collections: OffsetPaginated[CollectionType] = strawberry_django.offset_paginated()
    news: OffsetPaginated[NewsArticleType] = strawberry_django.offset_paginated(resolver=resolve_public_news)
    users: OffsetPaginated[UserType] = strawberry_django.offset_paginated()
    themes: list[ThemeType] = strawberry_django.field()
    characteristic_types: list[CharacteristicTypeType] = strawberry_django.field()
    characteristics: list[CharacteristicType] = strawberry_django.field()
    # TODO renommer en public_fictions, etc?

    # privé
    account: UserType = strawberry_django.auth.current_user()  # a son propre check d'auth
    # TODO private_fictions, etc? ou accès par account > created_fictions?


    # admin
    admin_fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(
        extensions=[IsStaff(fail_silently=False)],
    )
    admin_chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(
        extensions=[IsStaff(fail_silently=False)],
    )
    admin_chapter_versions: OffsetPaginated[ChapterVersionType] = strawberry_django.offset_paginated(
        resolver=resolve_admin_chapter_versions,
        extensions=[IsStaff(fail_silently=False)],
    )