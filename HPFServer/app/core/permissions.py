from rest_framework.permissions import BasePermission, SAFE_METHODS
from fictions.models import Beta


class HasBetaTurnOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return \
            (obj.stage == Beta.BetaStage.REQUESTED and request.user == obj.user) or \
            (obj.stage == Beta.BetaStage.ONGOING and request.user == obj.user) or \
            (obj.stage == Beta.BetaStage.CORRECTED and request.user in obj.chapter.authors.all())
