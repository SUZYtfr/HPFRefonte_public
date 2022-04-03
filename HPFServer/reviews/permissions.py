from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotRelatedToObjectOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        work = view.get_work()
        if request.user == work:
            return False
        elif hasattr(work, "authors") and request.user in work.authors.all():
            return False
        elif hasattr(work, "creation_user") and request.user == work.creation_user:
            return False
        return True


class IsAnonymousOrStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_anonymous:
            return True
        elif request.user.has_perm("reviews.can_post_review_as_staff"):
            return True
        return False


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.has_perm("reviews.can_post_review_as_staff"):
            return True
        return False


class HasNotReviewedAlready(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return True
        elif not view.get_work().reviews.filter(creation_user=request.user).exists():
            return True
        return False


class HasNotRepliedAlready(BasePermission):
    def has_permission(self, request, view):
        if not view.get_review().replies.filter(creation_user=request.user).exists():
            return True
        return False


class IsReviewOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.user == obj.creation_user:
            return True
        elif request.method in ["PUT", "PATCH"] and request.user.has_perm("reviews.change_review"):
            return True
        elif request.method == "DELETE" and request.user.has_perm("reviews.delete_review"):
            return True
        return False


class IsRelatedToReviewObjectOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        review = view.get_review()
        if request.user == review.creation_user:
            return False
        if review.replies.filter(creation_user=request.user).exists():
            return False

        work = review.work
        if request.user == work:
            return True
        if hasattr(work, "authors") and request.user in work.authors.all():
            return True
        elif hasattr(work, "creation_user") and request.user == work.creation_user:
            return True

        return False
