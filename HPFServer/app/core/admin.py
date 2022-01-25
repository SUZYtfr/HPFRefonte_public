from django.contrib import admin
from django.utils import timezone

admin.site.site_header = "Section d'administration HPF"


class BaseAdminAccess(admin.ModelAdmin):
    """Base d'accès d'administrateur"""

    def save_model(self, request, obj, form, change):
        """Sauvegarde le modèle: le créateur ou modificateur est l'utilisateur authentifié"""

        if obj.id:
            obj.modification_user = request.user
            obj.modification_date = timezone.now()
        else:
            obj.creation_user = request.user
            obj.creation_date = timezone.now()

        super().save_model(request, obj, form, change)
