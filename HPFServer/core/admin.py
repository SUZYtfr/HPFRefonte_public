from django.contrib.auth.models import Group
from django.contrib import admin
from django.utils import timezone

admin.site.site_header = "Section d'administration HPF"
admin.site.unregister(Group)


class BaseAdminPage(admin.ModelAdmin):
    """Base de page d'administrateur"""

    def save_model(self, request, obj, form, change):
        """Sauvegarde le modèle : le créateur ou modificateur est l'utilisateur authentifié"""

        if change:
            obj.modification_user = request.user
            obj.modification_date = timezone.now()
        else:
            obj.creation_user = request.user
            obj.creation_date = timezone.now()

        super().save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        metadata_fieldset = [
            ("Métadonnées", {
                "fields": [
                    ("creation_user", "creation_date"),
                    ("modification_user", "modification_date")
                ],
                "classes": ["collapse"]
            })
        ]
        fieldsets = list(super().get_fieldsets(request, obj))
        return fieldsets + metadata_fieldset

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        metadata_readonly_fields = ["creation_user", "creation_date", "modification_user", "modification_date"]

        return readonly_fields + metadata_readonly_fields
