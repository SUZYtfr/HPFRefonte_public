from rest_framework import viewsets, mixins, decorators, response

from .models import (
    FictionReview,
    ChapterReview,
    CollectionReview,
)
from .serializers import (
    FictionReviewSerializer,
    FictionReviewReplySerializer,
    ChapterReviewSerializer,
    ChapterReviewReplySerializer,
    CollectionReviewSerializer,
    CollectionReviewReplySerializer,
)

import logging
logging.basicConfig(level=logging.DEBUG)


class ReviewViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    pass


class ChapterReviewViewSet(ReviewViewSet):
    queryset = (
        ChapterReview.objects
        .published()
        .filter(level=0)
        .order_by("-creation_date")
    )
    serializer_class = ChapterReviewSerializer
    search_fields = ["chapter__title"]

    '''
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

    @decorators.action(
        detail=True,
        methods=["POST", "GET"],
        url_path="replies",
        serializer_class=ChapterReviewReplySerializer,
    )
    def manage_replies(self, request, *args, **kwargs):
        parent = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                parent=parent,
                creation_user=request.user,
            )
            return response.Response(data=serializer.data, status=201)
        else:
            replies = parent.get_descendants()
            serializer = self.get_serializer(replies, many=True)
            return response.Response(data=serializer.data)


class FictionReviewViewSet(ReviewViewSet):
    queryset = (
        FictionReview.objects
        .published()
        .filter(level=0)
        .order_by("-creation_date")
    )
    serializer_class = FictionReviewSerializer
    search_fields = ["fiction__title"]

    '''
    def get_queryset(self):
        if self.request.user.has_perm("view_reviews"):
            return super().get_queryset()
        if self.request.user.is_authenticated:
            return FictionReview.objects.filter(
                fiction__creation_user__user_preferences__member_review_policy__gte=UserPreferences.ReviewPolicy.SEE_TEXT,
            ).order_by("-creation_date")
        elif self.request.user.is_anonymous:
            return FictionReview.objects.filter(
                fiction__creation_user__user_preferences__anonymous_review_policy__gte=UserPreferences.ReviewPolicy.SEE_TEXT,
            )
    '''

    @decorators.action(
        detail=True,
        methods=["POST", "GET"],
        url_path="replies",
        serializer_class=FictionReviewReplySerializer,
    )
    def manage_replies(self, request, *args, **kwargs):
        parent = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                parent=parent,
                creation_user=request.user,    
            )
            return response.Response(data=serializer.data, status=201)
        else:
            replies = parent.get_descendants()
            serializer = self.get_serializer(replies, many=True)
            return response.Response(data=serializer.data)


class CollectionReviewViewSet(ReviewViewSet):
    queryset = (
        CollectionReview.objects
        .published()
        .filter(level=0)
        .order_by("-creation_date")
    )
    serializer_class = CollectionReviewSerializer
    search_fields = ["collection__title"]

    @decorators.action(
        detail=True,
        methods=["POST", "GET"],
        url_path="replies",
        serializer_class=CollectionReviewReplySerializer,
    )
    def manage_replies(self, request, *args, **kwargs):
        parent = self.get_object()

        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                parent=parent,
                creation_user=request.user,    
            )
            return response.Response(data=serializer.data, status=201)
        else:
            replies = parent.get_descendants()
            serializer = self.get_serializer(replies, many=True)
            return response.Response(data=serializer.data)
