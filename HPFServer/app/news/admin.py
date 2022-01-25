from django.contrib import admin

from core.admin import BaseAdminAccess

from .models import NewsArticle, NewsComment


class NewsAdminAccess(BaseAdminAccess):
    pass


class NewsCommentAccess(BaseAdminAccess):
    pass


admin.site.register(NewsArticle, NewsAdminAccess)
admin.site.register(NewsComment, NewsCommentAccess)
