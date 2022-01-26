from django.contrib import admin
from .models import Report


class ReportAdminAccess(admin.ModelAdmin):
    list_display = ("id", "argument", "status", "object",)
    fieldsets = (
        ("Signalement", {"fields": ("report_user", "datetime", "element", "argument", "object",)}),
        ("Traitement", {"fields": ("comment", "status",)}),
    )
    readonly_fields = ("id", "argument", "report_user", "datetime", "element", "object",)


admin.site.register(Report, ReportAdminAccess)
