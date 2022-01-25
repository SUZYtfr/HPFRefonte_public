from django.contrib import admin
from .models import Banner
from core.admin import BaseAdminAccess


class AdminAccess(BaseAdminAccess):
    pass


admin.site.register(Banner, AdminAccess)
