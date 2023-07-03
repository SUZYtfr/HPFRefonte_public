from django.utils import timezone
from django.db.models import F
from rest_framework import viewsets, response, decorators, mixins, permissions
from django_filters import rest_framework as filters

from users.models import UserPreferences
from reviews.utils import can_post_reviews, can_see_reviews
from reviews.serializers import (
    ChapterReviewSerializer,
    FictionReviewSerializer,
)

from .models import Collection, Fiction, Chapter
from .enums import ChapterValidationStage
from .serializers import (
    CollectionSerializer,
    FictionSerializer,
    ChapterSerializer,
    FictionTableOfContentsSerializer,
)
from .permissions import (
    IsAuthenticated,
    ReadOnly,
    IsCreationUser,
    IsFictionCoAuthor,
    IsParentFictionCreationUser,
    IsParentFictionCoAuthor,
    HasStaffValidation,
)
from .filters import FictionFilterSet

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
    search_fields = ["title", "fictions__title", "summary", "fictions__summary"]

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)


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
    permission_classes = [IsAuthenticated & (IsCreationUser | IsFictionCoAuthor) | ReadOnly]
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
        serializer_class=FictionTableOfContentsSerializer,
    )
    def get_table_of_contents(self, request, *args, **kwargs):
        fiction = self.get_object()
        serializer = self.get_serializer(instance=fiction)
        return response.Response(data=serializer.data)

    @decorators.action(
        detail=True,
        methods=["GET", "POST"],
        url_path="reviews",
        serializer_class=FictionReviewSerializer,
        permission_classes=[IsAuthenticated | ReadOnly],
    )
    def manage_reviews(self, request, *args, **kwargs):
        fiction = self.get_object()
        if request.method == "POST":
            if not can_post_reviews(fiction, request.user):
                raise
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(creation_user=self.request.user, fiction=fiction)
            return response.Response(data=serializer.validated_data)
        else:
            reviews = fiction.reviews.published() if can_see_reviews(fiction, request.user) else fiction.reviews.none()
            paginated_reviews = self.paginate_queryset(reviews)
            serializer = self.get_serializer(paginated_reviews, many=True)
            return response.Response(data=serializer.data)


class ChapterViewSet(viewsets.ModelViewSet):
    """Ensemble de vues publiques pour les chapitres"""

    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated & (IsParentFictionCreationUser | IsParentFictionCoAuthor) | ReadOnly]

    def get_queryset(self):
        """Détermine la liste des chapitres à afficher."""

        queryset = super().get_queryset()

        if self.request.user.has_perm("fictions.view_chapter"):
            return queryset.exclude(validation_status=ChapterValidationStage.DRAFT)
        elif self.request.query_params.get("self"):
            return queryset.filter(creation_user_id=self.request.user.id)
        else:
            return queryset.filter(validation_status=ChapterValidationStage.PUBLISHED)

    def get_object(self):
        """Renvoie le chapitre correspondant à l'ordre, incrémente son compte de lectures."""

        chapter = super().get_object()

        # https://docs.djangoproject.com/en/4.0/ref/models/expressions/#avoiding-race-conditions-using-f
        if all([
            self.action == "retrieve",
            self.request.user != chapter.fiction.creation_user,
            chapter.validation_status == ChapterValidationStage.PUBLISHED,
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
