import strawberry_django
from strawberry import auto, Info

from django.db.models import QuerySet, Q, F

from users.models import User
from news.models import NewsArticle
from fictions.models import Fiction, Chapter

from typing import Optional


@strawberry_django.filter_type(model=User, lookups=True)
class UserFilters:
    id: auto
    username: auto


@strawberry_django.filter_type(model=NewsArticle, lookups=True)
class NewsArticleFilters:
    title: auto
    post_date: auto


@strawberry_django.filter_type(model=Fiction, lookups=True)
class FictionFilters:
    title: auto
    creation_user: Optional["UserFilters"]
    last_update_date: auto


@strawberry_django.filter_type(model=Chapter, lookups=True)
class ChapterFilters:
    creation_user: Optional["UserFilters"]

    # La documentation officielle inclut le préfixe avant: {prefix}_title
    # Cependant dans mon cas ça semble fonctionner en le plaçant après: _title__{prefix}
    # Est-ce une erreur dans la documentation ? TODO vérifier
    @strawberry_django.filter_field(name="title")
    def title_lookups(
        self,
        info: Info,
        queryset: QuerySet[Chapter],
        value: strawberry_django.FilterLookup[str],
        prefix: str
    ) -> tuple[QuerySet[Chapter], Q]:
        queryset = queryset.alias(_title=F("published_version__title"))
        return strawberry_django.process_filters(
            filters=value,
            queryset=queryset,
            info=info,
            prefix=f"_title__{prefix}",
        )
