from django.db.models import QuerySet, Prefetch, Value, F, Q
from django.utils import timezone
import strawberry
import strawberry_django
from strawberry import Info
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import IsStaff, IsAuthenticated
from strawberry_django.auth.utils import get_current_user
from fictions.models import (
    Fiction,
    Chapter,
    ChapterVersion,
    Fandom,
    Collection,
    ChapterCollectionItem,
    FictionCollectionItem,
    CollectionCollectionItem,
)
from news.models import NewsArticle, NewsStatus
from reviews.models import ChapterReview, FictionReview, CollectionReview
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
    CollectionReviewType,
    CollectionItemType,
    ChapterCollectionItemType,
    FictionCollectionItemType,
    CollectionCollectionItemType,
)
from app.graphql_api.filters import SearchItemTypeFilter


# PUBLIQUE


def resolve_fandom_by_slug(slug: str) -> Fandom:
    return Fandom.objects.get(slug=slug)


def resolve_public_fictions(
    pk: strawberry.ID | None = None,
) -> QuerySet[Fiction] | Fiction:
    queryset = (
        Fiction.objects.published()
        .prefetch_related(
            Prefetch("chapters", Chapter.objects.published()),
        )
        .with_word_counts()
    )
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_public_chapters(
    pk: strawberry.ID | None = None,
) -> QuerySet[Chapter] | Chapter:
    queryset = Chapter.objects.published()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_public_collections(
    pk: strawberry.ID | None = None,
) -> QuerySet[Collection] | Collection:
    queryset = Collection.objects.all()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_public_fiction_reviews() -> QuerySet[FictionReview]:
    return FictionReview.objects.reviews().published()


def resolve_public_chapter_reviews() -> QuerySet[ChapterReview]:
    return ChapterReview.objects.reviews().published()


def resolve_public_collection_reviews() -> QuerySet[CollectionReview]:
    return CollectionReview.objects.reviews().published()


def resolve_public_news(
    pk: strawberry.ID | None = None,
) -> QuerySet[NewsArticle] | NewsArticle:
    queryset = NewsArticle.objects.filter(status=NewsStatus.PUBLISHED)
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


# PRIVÉ


def resolve_private_fictions(
    info: Info,
    pk: strawberry.ID | None = None,
) -> QuerySet[Fiction] | Fiction:
    current_user = get_current_user(info)
    queryset = current_user.created_fictions.all()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_private_chapters(
    info: Info,
    pk: strawberry.ID | None = None,
) -> QuerySet[Chapter] | Chapter:
    current_user = get_current_user(info)
    queryset = current_user.created_chapters.all()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


def resolve_private_collections(
    info: Info,
    pk: strawberry.ID | None = None,
) -> QuerySet[Collection] | Collection:
    current_user = get_current_user(info)
    queryset = current_user.created_collections.all()
    if pk:
        return queryset.get(pk=pk)
    else:
        return queryset


# ADMIN


def resolve_admin_chapter_versions() -> QuerySet[ChapterVersion]:
    return ChapterVersion.objects.exclude(submission_date__isnull=True)


# AUTRES


def resolve_itemtype_search(
    info: Info,
    filters: SearchItemTypeFilter,
) -> list[CollectionItemType]:
    """\
    Toutes les créations (séries, fictions, chapitres) en ItemType hors queryset.
    A utiliser dans le contexte de la création de série pour la recherche de nouveaux éléments.
    """

    current_user = get_current_user(info)

    element_filter = Q(creation_user__username__iexact=filters.creation_username)

    if filters.title:
        element_filter = element_filter & Q(title__icontains=filters.title)

    if filters.collection_id:
        element_filter = element_filter & ~Q(
            collections__parent_id=filters.collection_id,
        )

    fictions = (
        Fiction.objects.published()
        .filter(element_filter)
        .annotate(type=Value("fiction"), date=F("last_update_date"))
        .values("id", "type", "date")
        .order_by()
    )
    fictions = (
        fictions if not filters.types or "fiction" in filters.types else fictions.none()
    )
    chapters = (
        Chapter.objects.published()
        .filter(element_filter)
        .annotate(type=Value("chapitre"), date=F("publication_date"))
        .values("id", "type", "date")
        .order_by()
    )
    chapters = (
        chapters
        if not filters.types or "chapitre" in filters.types
        else chapters.none()
    )
    collections = (
        Collection.objects.filter(element_filter)
        .annotate(type=Value("série"), date=F("creation_date"))
        .values("id", "type", "date")
        .order_by()
    )
    collections = (
        collections
        if not filters.types or "série" in filters.types
        else collections.none()
    )
    ensemble = fictions.union(chapters).union(collections).order_by("-date")[:20]

    fake_items: list[CollectionItemType] = []
    for index, element in enumerate(ensemble):
        if element["type"] == "chapitre":
            fake_items.append(
                strawberry.cast(
                    ChapterCollectionItemType,
                    ChapterCollectionItem(
                        chapter_id=element["id"],
                        id=strawberry.UNSET,
                        order=0 - index,
                        is_accepted=False,
                        addition_date=timezone.now(),
                        addition_user=current_user,
                    ),
                ),
            )
        elif element["type"] == "fiction":
            fake_items.append(
                strawberry.cast(
                    FictionCollectionItemType,
                    FictionCollectionItem(
                        fiction_id=element["id"],
                        id=strawberry.UNSET,
                        order=0 - index,
                        is_accepted=False,
                        addition_date=timezone.now(),
                        addition_user=current_user,
                    ),
                ),
            )
        elif element["type"] == "série":
            fake_items.append(
                strawberry.cast(
                    CollectionCollectionItemType,
                    CollectionCollectionItem(
                        collection_id=element["id"],
                        id=strawberry.UNSET,
                        order=0 - index,
                        is_accepted=False,
                        addition_date=timezone.now(),
                        addition_user=current_user,
                    ),
                ),
            )

    return fake_items


@strawberry.type
class Query:
    # publique
    fandom_by_slug: FandomType = strawberry_django.field(
        resolver=resolve_fandom_by_slug,
    )
    fandoms: list[FandomType] = strawberry_django.field()
    fiction: FictionType = strawberry_django.field(resolver=resolve_public_fictions)
    fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(
        resolver=resolve_public_fictions,
    )
    chapter: ChapterType = strawberry_django.field(resolver=resolve_public_chapters)
    chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(
        resolver=resolve_public_chapters,
    )
    collection: CollectionType = strawberry_django.field(
        resolver=resolve_public_collections,
    )
    collections: OffsetPaginated[CollectionType] = strawberry_django.offset_paginated(
        resolver=resolve_public_collections,
    )
    fiction_reviews: OffsetPaginated[FictionReviewType] = (
        strawberry_django.offset_paginated(resolver=resolve_public_fiction_reviews)
    )
    chapter_reviews: OffsetPaginated[ChapterReviewType] = (
        strawberry_django.offset_paginated(resolver=resolve_public_chapter_reviews)
    )
    collection_reviews: OffsetPaginated[CollectionReviewType] = (
        strawberry_django.offset_paginated(resolver=resolve_public_collection_reviews)
    )
    news_article: NewsArticleType = strawberry_django.field(
        resolver=resolve_public_news,
    )
    news_articles: OffsetPaginated[NewsArticleType] = (
        strawberry_django.offset_paginated(resolver=resolve_public_news)
    )
    users: OffsetPaginated[UserType] = strawberry_django.offset_paginated()
    themes: list[ThemeType] = strawberry_django.field()
    characteristic_types: list[CharacteristicTypeType] = strawberry_django.field()
    characteristics: list[CharacteristicType] = strawberry_django.field()
    trigger_warnings: list[TriggerWarningType] = strawberry_django.field()
    # TODO renommer en public_fictions, etc?

    # privé
    account: UserType = (
        strawberry_django.auth.current_user()
    )  # a son propre check d'auth

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
    private_collection: CollectionType = strawberry_django.field(
        resolver=resolve_private_collections,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    private_collections: OffsetPaginated[CollectionType] = (
        strawberry_django.offset_paginated(
            resolver=resolve_private_collections,
            extensions=[IsAuthenticated(fail_silently=False)],
        )
    )
    # TODO private_fictions, etc? ou accès par account > created_fictions?

    # admin
    admin_fictions: OffsetPaginated[FictionType] = strawberry_django.offset_paginated(
        extensions=[IsStaff(fail_silently=False), IsAuthenticated(fail_silently=False)],
    )
    admin_chapters: OffsetPaginated[ChapterType] = strawberry_django.offset_paginated(
        extensions=[IsStaff(fail_silently=False), IsAuthenticated(fail_silently=False)],
    )
    admin_chapter_versions: OffsetPaginated[ChapterVersionType] = (
        strawberry_django.offset_paginated(
            resolver=resolve_admin_chapter_versions,
            extensions=[
                IsStaff(fail_silently=False),
                IsAuthenticated(fail_silently=False),
            ],
        )
    )

    # autres
    itemtype_search: list[CollectionItemType] = strawberry_django.field(
        resolver=resolve_itemtype_search,
        extensions=[IsAuthenticated(fail_silently=False)],
        description="Toutes les créations (séries, fictions, chapitres) en ItemType hors queryset",
    )
