from django.contrib import admin
from core.admin import BaseAdminAccess
from reviews.models import Review, ReviewReply


class ReviewAdminAccess(BaseAdminAccess):
    """Accès d'administration aux reviews"""

    list_display = ("id", "creation_user", "creation_date", "grading")
    fields = ("creation_user", "creation_date", "grading", "work",)
    readonly_fields = ("creation_user", "creation_date", "creation_date", "work",)

    def work(self, obj):
        return obj.work
    work.short_description = "sur"

    def depend_on(self, obj):
        return getattr(obj, "review") or getattr(obj, "parent")
    depend_on.short_description = "répond à"


class ReviewReplyAdminAccess(BaseAdminAccess):
    """Accès d'administration aux réponses à reviews"""

    list_display = ("id", "text", "creation_user",)
    fields = ("text", "creation_user", "depend_on",)
    readonly_fields = ("creation_user", "depend_on",)

    def depend_on(self, obj):
        return getattr(obj, "review") or getattr(obj, "parent")
    depend_on.short_description = "répond à"


# admin.site.register(Review, ReviewAdminAccess)
admin.site.register(ReviewReply, ReviewReplyAdminAccess)
