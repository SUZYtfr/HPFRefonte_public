from django.contrib import admin
from .models import (
    Banner,
    ProfilePicture,
    # NewsPicture,
    ContentImage,
)
from core.admin import BaseAdminAccess


class AdminAccess(BaseAdminAccess):
    pass


admin.site.register(Banner, AdminAccess)
admin.site.register(ProfilePicture, AdminAccess)
# admin.site.register(NewsPicture, AdminAccess)
admin.site.register(ContentImage, AdminAccess)
