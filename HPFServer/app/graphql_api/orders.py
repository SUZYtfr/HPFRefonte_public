from strawberry import auto
import strawberry_django

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


@strawberry_django.order_type(model=Chapter)
class ChapterOrder:
    title: auto  # FIXME ceci est un getter
    creation_date: auto
    modification_date: auto
    _order: auto = strawberry_django.order_field(name="order")


@strawberry_django.order_type(model=ChapterReview)
class ChapterReviewOrder:
    publication_date: auto


@strawberry_django.order_type(model=FictionReview)
class FictionReviewOrder:
    publication_date: auto
