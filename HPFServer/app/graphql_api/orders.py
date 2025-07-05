from strawberry import auto
import strawberry_django

from news.models import NewsArticle
from fictions.models import Fiction, Chapter


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
    _order: auto = strawberry_django.order_field(name="order")
