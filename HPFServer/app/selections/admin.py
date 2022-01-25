from django.contrib import admin
from .models import Selection, Proposition


class PropositionAdminAccess(admin.ModelAdmin):
    list_display = ("__str__", "selection",)
    readonly_fields = ("selection", "fiction", "proposed_by", "decided_by")

    def save_model(self, request, obj, form, change):
        """Sauvegarde la proposition : le créateur ou modificateur est l'utilisateur authentifié"""

        if obj.id:
            obj.decided_by = request.user
        else:
            obj.proposed_by = request.user

        super().save_model(request, obj, form, change)


admin.site.register(Selection)
admin.site.register(Proposition, PropositionAdminAccess)
