from strawberry import auto, Info
import strawberry_django

from django.db.models import QuerySet

from news.models import NewsArticle
from fictions.models import Fiction, Chapter
from reviews.models import ChapterReview, FictionReview


@strawberry_django.order_type(model=NewsArticle)
class NewsArticleOrder:
    post_date: auto


@strawberry_django.order_type(model=Fiction)
class FictionOrder:
    title: auto
    last_update_date: auto

    @strawberry_django.order_field
    def review_count(
        self,
        info: Info,
        queryset: QuerySet[Fiction],
        value: auto,
        prefix: str,
    ) -> tuple[QuerySet[Fiction] | list[str]]:
        queryset = queryset.with_review_counts()
        ordering = value.resolve(f"{prefix}_review_count")
        return queryset, [ordering]

    @strawberry_django.order_field
    def read_count(
        self,
        info: Info,
        queryset: QuerySet[Fiction],
        value: auto,
        prefix: str,
    ) -> tuple[QuerySet[Fiction] | list[str]]:
        queryset = queryset.with_read_counts()
        ordering = value.resolve(f"{prefix}_read_count")
        return queryset, [ordering]

    @strawberry_django.order_field
    def average(
        self,
        info: Info,
        queryset: QuerySet[Fiction],
        value: auto,
        prefix: str,
    ) -> tuple[QuerySet[Fiction] | list[str]]:
        queryset = queryset.with_averages()
        ordering = value.resolve(f"{prefix}_average")
        return queryset, [ordering]


@strawberry_django.order_type(model=Chapter)
class ChapterOrder:
    title: auto
    creation_date: auto
    modification_date: auto
    _order: auto = strawberry_django.order_field(name="order")


@strawberry_django.order_type(model=ChapterReview)
class ChapterReviewOrder:
    publication_date: auto


@strawberry_django.order_type(model=FictionReview)
class FictionReviewOrder:
    publication_date: auto
