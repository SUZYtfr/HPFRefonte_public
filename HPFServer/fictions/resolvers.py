from fictions.models import Fiction
from fictions.types import PaginatedFictionType
from math import ceil


def resolve_paginated_fictions(
    root,
    info,
    page_size: int,
    page: int,
    search_author: str | None = None,
    search_author_id: int | None = None,
) -> PaginatedFictionType:
    page_size = page_size
    offset = page_size * page
    initial_fictions = Fiction.objects.published()
    if search_author:
        initial_fictions = initial_fictions.filter(
            creation_user__username=search_author,
        )
    if search_author_id:
        initial_fictions = initial_fictions.filter(
            creation_user_id=search_author_id,
        )
    current_page = ceil(offset / page_size) + 1
    total_pages = ceil(initial_fictions.count() / page_size)
    subset_fictions = initial_fictions[offset:offset+page_size]

    return PaginatedFictionType(
        results=subset_fictions,
        count=initial_fictions.count(),
        current=current_page,
        # pageSize=page_size,
        # currentPage=current_page,
        # totalPages=total_pages,
    )
