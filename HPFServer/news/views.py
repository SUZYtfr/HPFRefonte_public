from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters import rest_framework as filters

from core.permissions import DjangoPermissionOrReadOnly, IsObjectCreatorOrReadOnly
from .models import NewsArticle, NewsComment
from .enums import NewsStatus
from .serializers import NewsArticleSerializer, NewsCommentSerializer
from .filters import NewsArticleFilterSet
from core.utils import get_moderation_account


class PublicNewsViewSet(ReadOnlyModelViewSet):
    """Ensemble de vues publiques d'actualités"""

    queryset = NewsArticle.objects.filter(status=NewsStatus.PUBLISHED).order_by("-post_date")
    serializer_class = NewsArticleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NewsArticleFilterSet


class PrivateNewsViewSet(ModelViewSet):
    """Ensemble de vues publiques d'actualités"""

    # permission_classes = [IsStaff]
    queryset = NewsArticle.objects.order_by("-creation_date")
    serializer_class = NewsArticleSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NewsArticleFilterSet

    def perform_create(self, serializer):
        serializer.save(
            # creation_user=self.request.user,
            creation_user=get_moderation_account(),
            creation_date=timezone.now(),
        )

    def perform_update(self, serializer):
        serializer.save(
            # creation_user=self.request.user,
            modification_user=get_moderation_account(),
            modification_date=timezone.now(),
        )


class NewsCommentViewSet(ModelViewSet):
    """Ensemble de vues de commentaires d'actualités"""

    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectCreatorOrReadOnly]
    serializer_class = NewsCommentSerializer
    queryset = NewsComment.objects.all()

    def get_queryset(self):
        if self.request.user.has_perm("news.view_newsarticle"):
            return self.queryset.filter(
                newsarticle_id=self.kwargs["news_pk"],
            )
        else:
            return self.queryset.filter(
                newsarticle_id=self.kwargs["news_pk"],
                newsarticle__status=NewsStatus.PUBLISHED
            )

    def perform_create(self, serializer):
        serializer.save(
            newsarticle_id=self.kwargs["news_pk"],
            creation_user=self.request.user,
            creation_date=timezone.now(),
        )

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())
