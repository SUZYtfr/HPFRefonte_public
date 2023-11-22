from django.db.models import Q, Subquery
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from django_filters.rest_framework import DjangoFilterBackend

from .models import BaseReview
from .serializers import AllReviewSerializer
from .filters import ReviewFilterset

import logging
logging.basicConfig(level=logging.DEBUG)


'''
    """
    Queryset filtrant les reviews selon le droit de visibilité accordé par leurs auteurs
    """
    def get_queryset(self):
        if self.request.user.has_perm("view_reviews"):
            return super().get_queryset()
        if self.request.user.is_authenticated:
            return ChapterReview.objects.filter(
                chapter__creation_user__preferences__member_review_policy__gte=UserPreferences.ReviewPolicy.SEE_TEXT,
            ).order_by("-creation_date")
        elif self.request.user.is_anonymous:
            return ChapterReview.objects.filter(
                chapter__creation_user__preferences__anonymous_review_policy__gte=UserPreferences.ReviewPolicy.SEE_TEXT,
            )
    '''


class ReviewViewset(ModelViewSet):
    """Ensemble de vues de tous types de reviews"""

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = BaseReview.objects.reviews().published().order_by("-creation_date")
    serializer_class = AllReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilterset

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)

    @action(
        detail=True,
        methods=["GET", "POST"],
        url_path="replies",
        url_name="replies",
        queryset=BaseReview.objects.all(),
    )
    def manage_replies(self, request, *args, **kwargs):
        """Vue de gestion des réponses à reviews de l'élément."""

        parent = self.get_object()
        
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(parent=parent, creation_user=request.user)
            return Response(data=serializer.data, status=HTTP_201_CREATED)
        else:
            replies = parent.get_descendants()
            serializer = self.get_serializer(replies, many=True)
            return Response(data=serializer.data)

    @action(
        detail=True,
        methods=["GET"],
        url_path="context",
        url_name="context",
        queryset=BaseReview.objects.all(),
    )
    def get_context(self, *args, **kwargs):
        """Vue de récupération de l'arbre menant à l'élément."""

        draft_basereview = self.get_object()
        root_node = draft_basereview.get_root()
        serializer = self.get_serializer(instance=root_node, many=False)
        return Response(serializer.data)

    def perform_update(self, serializer, *args, **kwargs):
        serializer.save(modification_user=self.request.user)


class BaseAccountReviewViewset(ReadOnlyModelViewSet):
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    serializer_class = AllReviewSerializer
    filterset_class = ReviewFilterset


class AccountPublishedReviewViewset(BaseAccountReviewViewset):
    """Ensemble de vues de tous types de reviews publiées par le compte."""

    def get_queryset(self, *args, **kwargs):
        reviews_created_by_user = BaseReview.objects.reviews().filter(creation_user=self.request.user)
        return reviews_created_by_user.order_by("-creation_date")


class AccountReceivedReviewViewset(BaseAccountReviewViewset):
    """Ensemble de vues de tous types de reviews reçues par le compte."""

    def get_queryset(self, *args, **kwargs):
        reviews_received_by_user = BaseReview.objects.reviews().filter(
            Q(CollectionReview___collection__creation_user=self.request.user)
            |
            Q(FictionReview___fiction__creation_user=self.request.user)
            |
            Q(ChapterReview___chapter__creation_user=self.request.user)
        )
        return reviews_received_by_user.published().order_by("-creation_date")


class AccountDraftReviewViewset(BaseAccountReviewViewset):
    """Ensemble de vues de tous types de reviews et réponses à reviews en brouillon par le compte."""

    def get_queryset(self, *args, **kwargs):
        draft_basereviews_by_user = BaseReview.objects.filter(
            creation_user=self.request.user,
            is_draft=True,
        )
        return draft_basereviews_by_user.order_by("-creation_date")


class AccountUnansweredReviewViewset(BaseAccountReviewViewset):
    """Ensemble de vues de tous types de reviews et réponses à reviews non répondues par le compte."""

    def get_queryset(self, *args, **kwargs):
        tree_ids_with_user = (
            BaseReview
            .objects
            .filter(creation_user=self.request.user)
            .values("tree_id")
            .order_by()
            .distinct()
        )
        unanswered_nodes_not_by_user = (
            BaseReview
            .objects
            .leaves()
            .non_archived()
            .filter(is_draft=False)
            .exclude(creation_user=self.request.user)
            .filter(tree_id__in=Subquery(tree_ids_with_user))
        )
        return unanswered_nodes_not_by_user
