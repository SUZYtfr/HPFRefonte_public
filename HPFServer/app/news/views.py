from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission, SAFE_METHODS

from .models import NewsArticle, NewsComment
from .serializers import NewsSerializer, NewsCommentSerializer


class IsCreatorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if (request.method in SAFE_METHODS) or (request.user == obj.creation_user):
            return True
        return False


class NewsListView(ListAPIView):
    """Vue de listage d'actualités"""

    queryset = NewsArticle.objects.filter(status=NewsArticle.NewsStatus.PUBLISHED).order_by("-post_date")
    serializer_class = NewsSerializer


class NewsCommentViewSet(ModelViewSet):
    """Ensemble de vues de commentaires d'actualités"""

    permission_classes = (IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly,)
    queryset = NewsComment.objects
    serializer_class = NewsCommentSerializer
