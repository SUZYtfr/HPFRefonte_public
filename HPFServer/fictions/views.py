from django.utils import timezone
from django.db.models import F
from django.conf import settings
from rest_framework import (
    viewsets,
    response,
    decorators,
    mixins,
    permissions,
    status,
)
from django_filters import rest_framework as filters

from core.pagination import CurrentPagePagination
from users.models import UserPreferences
from reviews.serializers import (
    FictionReviewSerializer,
    ChapterReviewSerializer,
    CollectionReviewSerializer,
)

from fictions.models import (
    Collection,
    Fiction,
    Chapter,
    ChapterVersion,
)
from fictions.enums import ChapterValidationStage
from fictions.serializers import (
    CollectionSerializer,
    FictionSerializer,
    ChapterSerializer,
    FictionTableOfContentsSerializer,
    PrivateChapterSerializer,
    PrivateChapterVersionListSerializer,
)
from fictions.permissions import (
    IsAuthenticated,
    ReadOnly,
    IsParentFictionCreationUser,
    IsParentFictionCoAuthor,
)
from fictions.filters import FictionFilterSet, ChapterFilterSet

import logging
logging.basicConfig(level=logging.DEBUG)


class AuthorPreferenceAllowsAnonymousReviews(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.creation_user.preferences.anonymous_review_policy >= UserPreferences.ReviewPolicy.WRITE_TEXT:
            return True
        return False


class AuthorPreferenceAllowsMemberReviews(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.creation_user.preferences.member_review_policy >= UserPreferences.ReviewPolicy.WRITE_TEXT:
            return True
        return False


class CollectionViewSet(viewsets.ModelViewSet):
    """Ensemble de vues pour les séries"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.order_by("-creation_date")
    search_fields = ["title", "summary"]

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)

    # TODO - dégager ça, passer par /reviews/reviews/
    @decorators.action(
        detail=True,
        methods=["POST", "GET"],
        url_path="reviews",
        url_name="reviews",
        serializer_class=CollectionReviewSerializer,
    )
    def manage_reviews(self, request, *args, **kwargs):
        collection = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(collection=collection, creation_user=self.request.user)
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            published_reviews = collection.reviews.published()
            paginated_reviews = self.paginate_queryset(published_reviews)
            serializer = self.get_serializer(paginated_reviews, many=True)
            paginated_serializer = self.get_paginated_response(data=serializer.data)
            return response.Response(data=paginated_serializer.data)


class FictionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """Ensemble de vues pour les fictions"""
    queryset = (
        Fiction.objects
        .with_averages()
        .with_word_counts()
        .with_review_counts()
        .order_by("-creation_date")
    )
    serializer_class = FictionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = FictionFilterSet

    def get_queryset(self):
        """Détermine la liste de fictions à afficher."""

        queryset = super().get_queryset()

        if self.request.user.has_perm("fictions.view_fiction"):
            return queryset
        elif self.request.query_params.get("self"):
            return queryset.filter(creation_user_id=self.request.user.id)
        else:
            return queryset.published()

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)

    @decorators.action(
        detail=True,
        methods=["GET"],
        url_path="table-of-contents",
        url_name="table-of-contents",
        serializer_class=FictionTableOfContentsSerializer,
    )
    def get_table_of_contents(self, request, *args, **kwargs):
        fiction = self.get_object()
        serializer = self.get_serializer(instance=fiction)
        return response.Response(data=serializer.data)

    # TODO - dégager ça, passer par /reviews/reviews/
    @decorators.action(
        detail=True,
        methods=["POST", "GET"],
        url_path="reviews",
        url_name="reviews",
        serializer_class=FictionReviewSerializer,
    )
    def manage_reviews(self, request, *args, **kwargs):
        fiction = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(fiction=fiction, creation_user=self.request.user)
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            published_reviews = fiction.reviews.published()
            paginated_reviews = self.paginate_queryset(published_reviews)
            serializer = self.get_serializer(paginated_reviews, many=True)
            paginated_serializer = self.get_paginated_response(data=serializer.data)
            return response.Response(data=paginated_serializer.data)


class PublicChapterViewSet(viewsets.ModelViewSet):
    """Ensemble de vues publiques pour les chapitres"""

    queryset = Chapter.objects.published()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated & (IsParentFictionCreationUser | IsParentFictionCoAuthor) | ReadOnly]

    def get_object(self) -> Chapter:
        """Renvoie le chapitre correspondant à l'ordre, incrémente son compte de lectures."""

        chapter: Chapter = super().get_object()

        # https://docs.djangoproject.com/en/4.0/ref/models/expressions/#avoiding-race-conditions-using-f
        if all([
            self.action == "retrieve",
            self.request.user != chapter.fiction.creation_user,
            chapter.is_published,
        ]):
            chapter.read_count = F("read_count") + 1
            chapter.save_base()
            chapter.refresh_from_db(fields=["read_count"])

        return chapter

    def perform_create(self, serializer):
        serializer.save(
            fiction_id=self.kwargs["fiction_pk"],
            creation_user=self.request.user,
            creation_date=timezone.now(),
        )

    def perform_update(self, serializer):
        serializer.save(
            modification_user=self.request.user,
            modification_date=timezone.now(),
        )

    # TODO - dégager ça, passer par /reviews/reviews/
    @decorators.action(
        detail=True,
        methods=["POST", "GET"],
        url_path="reviews",
        url_name="reviews",
        serializer_class=ChapterReviewSerializer,
    )
    def manage_reviews(self, request, *args, **kwargs):
        chapter = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(chapter=chapter, creation_user=self.request.user)
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            published_reviews = chapter.reviews.published()
            paginated_reviews = self.paginate_queryset(published_reviews)
            serializer = self.get_serializer(paginated_reviews, many=True)
            paginated_serializer = self.get_paginated_response(data=serializer.data)
            return response.Response(data=paginated_serializer.data)


class PrivateChapterViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Chapter.objects.all()
    serializer_class = PrivateChapterSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ChapterFilterSet
    # permission_classes - TODO


class PrivateChapterTextVersionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ChapterVersion.objects.all()
    serializer_class = PrivateChapterVersionListSerializer
