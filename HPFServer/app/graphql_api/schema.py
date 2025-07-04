import strawberry
import strawberry_django
from strawberry_django.optimizer import DjangoOptimizerExtension
from strawberry_django_extras import JWTMutations
from strawberry_django.permissions import IsAuthenticated, IsStaff
from strawberry_django.pagination import OffsetPaginated

from app.graphql_api.types import (
    FictionType,
    ChapterType,
    CollectionType,
    UserType,
    ThemeType,
    CharacteristicTypeType,
    NewsArticleType,
)
from app.graphql_api.resolvers import resolve_public_fictions, resolve_public_chapters
from app.graphql_api.mutations import (
    post_comment,
    create_fiction,
    update_fiction,
    delete_fiction,
    create_chapter,
    update_chapter,
    delete_chapter,
    invalidate_chapter_version,
)


""" 
TODO :
- permission IsOwner(target_fields=[creation_user, authors, etc.]) (ex. ChapterVersion)
- exceptions mieux définies ? IllogicalActionError ?
- Session data corrupted??
- (postman) authentification plus simple
- choix du meilleur système pour les accès:
    - routes séparées (/graphql/public/, /graphql/private/, /graphql/admin/)
    - racines séparées (published_fictions, private_fictions, admin_fictions) *
    - unique, accès de champs par filtres et permissions
    * système appliqué pour le moment
"""


@strawberry.type
class Query:
    # publique
    fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(resolver=resolve_public_fictions)
    chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(resolver=resolve_public_chapters)
    collections: OffsetPaginated[CollectionType] = strawberry_django.offset_paginated()
    news: OffsetPaginated[NewsArticleType] = strawberry_django.offset_paginated()
    users: OffsetPaginated[UserType] = strawberry_django.offset_paginated()
    themes: list[ThemeType] = strawberry_django.field()
    characteristic_types: list[CharacteristicTypeType] = strawberry_django.field()

    # privé
    account: UserType = strawberry_django.auth.current_user()  # a son propre check d'auth

    # admin
    all_fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(
        extensions=[IsStaff()],
    )
    all_chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(
        extensions=[IsStaff()],
    )
    

@strawberry.type
class Mutation:
    # publique
    request_token = JWTMutations.issue

    # privé
    post_comment = strawberry_django.mutation(
        resolver=post_comment,
        extensions=[IsAuthenticated()],
    )
    create_fiction = strawberry_django.mutation(
        resolver=create_fiction,
        extensions=[IsAuthenticated()],
    )
    update_fiction = strawberry_django.mutation(
        resolver=update_fiction,
        extensions=[IsAuthenticated()],
    )
    delete_fiction = strawberry_django.mutation(
        resolver=delete_fiction,
        extensions=[IsAuthenticated()],
    )
    create_chapter = strawberry_django.mutation(
        resolver=create_chapter,
        extensions=[IsAuthenticated()],
    )
    update_chapter = strawberry_django.mutation(
        resolver=update_chapter,
        extensions=[IsAuthenticated()],
    )
    delete_chapter = strawberry_django.mutation(
        resolver=delete_chapter,
        extensions=[IsAuthenticated()],
    )

    # private
    invalidate_chapter_version = strawberry_django.mutation(
        resolver=invalidate_chapter_version,
        extensions=[IsStaff()],
    )

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        DjangoOptimizerExtension,
    ],
)
