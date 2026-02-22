import strawberry_django
from strawberry import auto, Info, ID

from django.db.models import QuerySet, Q, F, Count

from users.models import User
from news.models import NewsArticle
from fictions.models import Fiction, Chapter, Fandom
from characteristics.models import Characteristic
from reviews.models import ChapterReview, FictionReview

from typing import Optional


@strawberry_django.filter_type(model=User, lookups=True)
class UserFilters:
    id: auto
    username: auto


@strawberry_django.filter_type(model=NewsArticle, lookups=True)
class NewsArticleFilters:
    id: auto
    title: auto
    post_date: auto
    creation_user: Optional["UserFilters"]


@strawberry_django.filter_type(model=Fiction, lookups=True)
class FictionFilters:
    id: auto
    title: auto
    creation_user: Optional["UserFilters"]
    last_update_date: auto
    status: auto
    featured: auto
    fandoms: Optional["FandomFilters"]
    characteristics: Optional["CharacteristicFilters"]


@strawberry_django.filter_type(model=Chapter, lookups=True)
class ChapterFilters:
    id: auto
    creation_user: Optional["UserFilters"]

    # La documentation officielle inclut le préfixe avant: {prefix}_title
    # Cependant dans mon cas ça semble fonctionner en le plaçant après: _title__{prefix}
    # Est-ce une erreur dans la documentation ? TODO vérifier
    @strawberry_django.filter_field(name="title")
    def title_lookups(
        self,
        info: Info,
        queryset: QuerySet[Chapter],
        # FIXME - remplacer par strawberry_django.FilterLookup[str] quand ce bug connu sera corrigé :
        # https://github.com/strawberry-graphql/strawberry-django/issues/845
        value: strawberry_django.fields.filter_types.StrFilterLookup[str],
        prefix: str,
    ) -> tuple[QuerySet[Chapter], Q]:
        queryset = queryset.alias(_title=F("published_version__title"))
        return strawberry_django.process_filters(
            filters=value,
            queryset=queryset,
            info=info,
            prefix=f"_title__{prefix}",
        )


@strawberry_django.filter_type(model=ChapterReview, lookups=True)
class ChapterReviewFilters:
    id: auto
    chapter: Optional["ChapterFilters"]


@strawberry_django.filter_type(model=FictionReview, lookups=True)
class FictionReviewFilters:
    id: auto
    fiction: Optional["FictionFilters"]


@strawberry_django.filter_type(model=Fandom, lookups=True)
class FandomFilters:
    id: auto
    name: auto
    slug: auto

    @strawberry_django.filter_field(name="allIdsInList")
    def all_ids_in_list_lookup(
        self,
        info: Info,
        queryset: QuerySet[Fiction],
        value: list[ID],
        prefix: str,
    ) -> tuple[QuerySet[Fiction], Q]:
        number_of_matching_fandoms = Count(
            "fandoms",
            filter=Q(fandoms__pk__in=value),
            distinct=True,
        )

        queryset = queryset.alias(
            number_of_matching_fandoms=number_of_matching_fandoms,
        )
        q = Q(number_of_matching_fandoms=len(value))

        return queryset, q


@strawberry_django.filter_type(model=Characteristic, lookups=True)
class CharacteristicFilters:
    id: auto

    @strawberry_django.filter_field(name="allIdsInList")
    def all_ids_in_list_lookup(
        self,
        info: Info,
        queryset: QuerySet[Fiction],
        value: list[ID],
        prefix: str,
    ) -> tuple[QuerySet[Fiction], Q]:
        number_of_matching_characteristics = Count(
            "characteristics",
            filter=Q(characteristics__pk__in=value),
            distinct=True,
        )

        queryset = queryset.alias(
            number_of_matching_characteristics=number_of_matching_characteristics,
        )
        q = Q(number_of_matching_characteristics=len(value))

        return queryset, q
