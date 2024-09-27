from news.models import NewsArticle
from news.types import PaginatedNewsArticlesType

from math import ceil


def resolve_news_article(root, info, news_id: int) -> NewsArticle:
    return NewsArticle.objects.get(pk=news_id)


def resolve_paginated_news_articles(
    root,
    info,
    page: int,
    page_size: int,
) -> PaginatedNewsArticlesType:
    offset = page_size * page
    initial_news_articles = NewsArticle.objects.all()
    current_page = ceil(offset / page_size) + 1
    total_pages = ceil(initial_news_articles.count() / page_size)
    subset_news_articles = initial_news_articles[offset:offset+page_size]

    return PaginatedNewsArticlesType(
        results=subset_news_articles,
        count=initial_news_articles.count(),
        current=current_page,
    )
