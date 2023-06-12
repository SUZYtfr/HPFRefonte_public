from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.permissions import DjangoPermissionOrReadOnly, IsObjectCreatorOrReadOnly
from .models import NewsArticle, NewsComment
from .serializers import NewsArticleSerializer, NewsCommentSerializer
from .enums import NewsStatus


class NewsViewSet(ModelViewSet):
    """Ensemble de vues d'actualités"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticatedOrReadOnly, DjangoPermissionOrReadOnly]
    queryset = NewsArticle.objects.filter(status=NewsStatus.PUBLISHED).order_by("-post_date")
    serializer_class = NewsArticleSerializer

    def get_queryset(self):
        if self.request.user.has_perm("news.view_newsarticle"):
            return NewsArticle.objects.order_by("-creation_date")
        return self.queryset

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())


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
