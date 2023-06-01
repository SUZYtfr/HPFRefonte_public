from rest_framework import viewsets, mixins, generics, exceptions, permissions, decorators

from users.models import User, UserPreferences

from core.utils import get_moderation_account
from fictions.models import Fiction, Chapter, Collection
from .models import Review, ReviewReply, FictionReview, ChapterReview, CollectionReview
from .serializers import ReviewSerializer, AnonymousReviewSerializer, StaffReviewSerializer, \
    ReviewReplySerializer, ReviewTextSerializer, StaffReviewReplySerializer, ChapterReviewSerializer, CollectionReviewSerializer, FictionReviewSerializer, ChapterAnonymousReviewSerializer, FictionAnonymousReviewSerializer, CollectionAnonymousReviewSerializer
from .permissions import IsNotRelatedToObjectOrReadOnly, IsReviewOwnerOrReadOnly, IsRelatedToReviewObjectOrReadOnly, \
    IsAnonymousOrStaffOrReadOnly, HasNotReviewedAlready, IsStaffOrReadOnly, HasNotRepliedAlready

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
    queryset = ChapterReview.objects.filter(draft=False).order_by("-creation_date")
    serializer_class = ChapterReviewSerializer
    search_fields = ["chapter__title"]

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


class FictionReviewViewSet(ReviewViewSet):
    serializer_class = FictionReviewSerializer
    search_fields = ["fiction__title"]
    queryset = FictionReview.objects.published().order_by("-creation_date")

    def get_queryset(self):
        if self.request.user.has_perm("view_reviews"):
            return super().get_queryset()
        if self.request.user.is_authenticated:
            return FictionReview.objects.filter(
                fiction__creation_user__preferences__member_review_policy__gte=UserPreferences.ReviewPolicy.SEE_TEXT,
            ).order_by("-creation_date")
        elif self.request.user.is_anonymous:
            return FictionReview.objects.filter(
                fiction__creation_user__preferences__anonymous_review_policy__gte=UserPreferences.ReviewPolicy.SEE_TEXT,
            )


class CollectionReviewViewSet(ReviewViewSet):
    queryset = CollectionReview.objects.filter(draft=False).order_by("-creation_date")
    serializer_class = CollectionReviewSerializer
    search_fields = ["collection__title"]


# TODO - décortiquer ça et supprimer
# class ObjectReviewListCreateView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
#     """Vue de création et de listage de reviews pour un objet"""
#
#     serializer_class = ReviewSerializer
#     permission_classes = [HasNotReviewedAlready & (IsAnonymousOrStaffOrReadOnly | IsNotRelatedToObjectOrReadOnly)]
#
#     def get_work(self):
#         model_name = self.kwargs["model_name"]
#         work = ContentType.objects.get(model=model_name).get_object_for_this_type(pk=self.kwargs["object_pk"])
#         return work
#
#     def get_queryset(self):
#         work = self.get_work()
#         return work.reviews.filter(draft=False).order_by("-creation_date")
#
#     def get_serializer_class(self):
#         if self.action == "create":
#             if self.request.user.is_anonymous:
#                 return AnonymousReviewSerializer
#             elif self.request.user.has_perm("reviews.can_post_review_as_staff"):
#                 return StaffReviewSerializer
#             else:
#                 return self.serializer_class
#         return self.serializer_class
#
#     def perform_create(self, serializer):
#         creation_user = self.request.user
#
#         # Ces deux contrôles peuvent potentiellement changer le créateur de la review
#         if serializer.validated_data.pop("as_staff"):
#             creation_user = get_moderation_account()
#
#         elif email := serializer.validated_data.pop("email", None):
#             try:
#                 creation_user = User.objects.get(
#                     email=email,  # Cet e-mail est-il déjà connu ?
#                 )
#
#                 if creation_user.is_active:  # Si oui, et c'est un compte actif, imposer l'authentification
#                     raise exceptions.NotAuthenticated("Un compte actif existe avec cette adresse e-mail.")
#
#             except User.DoesNotExist:
#                 creation_user = User.objects.create_anonymous_user(
#                     email=email,  # Si non, on crée le compte anonymisé
#                 )
#
#         # On revérifie l'absence de double-review avec l'utilisateur anonyme ou le compte de modération
#         work = self.get_work()
#         if work.reviews.filter(creation_user=creation_user).exists():
#             self.permission_denied(request=self.request)
#
#         serializer.save(creation_user=creation_user, creation_date=timezone.now(), work=work)
#
#
# class ReviewsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
#     """Ensemble de vues de reviews"""
#
#     serializer_class = ReviewSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
#     # queryset = Review.objects.filter(draft=False).order_by("-creation_date")
#     search_fields = ["creation_user__username"]
#
#     def perform_update(self, serializer):
#         serializer.save(modification_user=self.request.user, modification_date=timezone.now())
#
#     def get_queryset(self):
#         if self.request.query_params.get("mine", False) == "True":
#             return Review.objects.filter(creation_user=self.request.user.id)
#         return self.queryset
#
#
# class MyPersonalReviewHistoryView(generics.ListAPIView):
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = ReviewTextSerializer
#
#     def get_queryset(self):
#         return Review.objects.filter(creation_user=self.request.user).get(pk=self.kwargs["pk"]).versions.all()


class ReplyViewSet(viewsets.ModelViewSet):
    # permission_classes = [HasNotRepliedAlready & (IsStaffOrReadOnly | IsRelatedToReviewObjectOrReadOnly)]
    serializer_class = ReviewReplySerializer

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs["review_pk"],
            draft=False,
        )

    def get_queryset(self):
        return self.get_review().replies.all()

    def get_serializer_class(self):
        if self.request.user.has_perm("reviews.can_post_review_as_staff"):
            return StaffReviewReplySerializer
        return self.serializer_class

    def perform_create(self, serializer):
        creation_user = self.request.user

        if serializer.validated_data.pop("as_staff"):
            creation_user = get_moderation_account()

        review = self.get_review()
        if review.replies.filter(creation_user=creation_user).exists():
            self.permission_denied(request=self.request)

        serializer.save(creation_user=creation_user, creation_date=timezone.now(), review=review)

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())
