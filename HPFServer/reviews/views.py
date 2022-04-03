from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.exceptions import NotAuthenticated

from users.models import User

from core.models import get_moderation_account
from .models import Review, ReviewReply
from .serializers import ReviewSerializer, AnonymousReviewSerializer, StaffReviewSerializer, \
    ReviewReplySerializer, ReviewTextSerializer, StaffReviewReplySerializer
from .permissions import IsNotRelatedToObjectOrReadOnly, IsReviewOwnerOrReadOnly, IsRelatedToReviewObjectOrReadOnly, \
    IsAnonymousOrStaffOrReadOnly, HasNotReviewedAlready, IsStaffOrReadOnly, HasNotRepliedAlready

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.shortcuts import get_object_or_404


class ModelReviewListView(ListAPIView):
    """Vue de listage de reviews pour un modèle"""

    serializer_class = ReviewSerializer

    def get_queryset(self):
        model_name = self.kwargs.get("model_name")
        content_type_id = ContentType.objects.get(model=model_name).id
        return Review.objects.filter(content_type_id=content_type_id, draft=False).order_by("-creation_date")


class ObjectReviewListCreateView(GenericViewSet, ListModelMixin, CreateModelMixin):
    """Vue de création et de listage de reviews pour un objet"""

    serializer_class = ReviewSerializer
    permission_classes = [HasNotReviewedAlready & (IsAnonymousOrStaffOrReadOnly | IsNotRelatedToObjectOrReadOnly)]

    def get_work(self):
        model_name = self.kwargs["model_name"]
        work = ContentType.objects.get(model=model_name).get_object_for_this_type(pk=self.kwargs["object_pk"])
        return work

    def get_queryset(self):
        work = self.get_work()
        return work.reviews.filter(draft=False).order_by("-creation_date")

    def get_serializer_class(self):
        if self.action == "create":
            if self.request.user.is_anonymous:
                return AnonymousReviewSerializer
            elif self.request.user.has_perm("reviews.can_post_review_as_staff"):
                return StaffReviewSerializer
            else:
                return self.serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        creation_user = self.request.user

        # Ces deux contrôles peuvent potentiellement changer le créateur de la review
        if serializer.validated_data.pop("as_staff"):
            creation_user = get_moderation_account()

        elif email := serializer.validated_data.pop("email", None):
            try:
                creation_user = User.objects.get(
                    email=email,  # Cet e-mail est-il déjà connu ?
                )

                if creation_user.is_active:  # Si oui, et c'est un compte actif, imposer l'authentification
                    raise NotAuthenticated("Un compte actif existe avec cette adresse e-mail.")

            except User.DoesNotExist:
                creation_user = User.objects.create_anonymous_user(
                    email=email,  # Si non, on crée le compte anonymisé
                )

        # On revérifie l'absence de double-review avec l'utilisateur anonyme ou le compte de modération
        work = self.get_work()
        if work.reviews.filter(creation_user=creation_user).exists():
            self.permission_denied(request=self.request)

        serializer.save(creation_user=creation_user, creation_date=timezone.now(), work=work)


class ReviewsViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    """Ensemble de vues de reviews"""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewOwnerOrReadOnly]
    queryset = Review.objects.filter(draft=False).order_by("-creation_date")
    search_fields = ["creation_user__nickname"]

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())

    def get_queryset(self):
        if self.request.query_params.get("mine", False) == "True":
            return Review.objects.filter(creation_user=self.request.user.id)
        return self.queryset


class MyPersonalReviewHistoryView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewTextSerializer

    def get_queryset(self):
        return Review.objects.filter(creation_user=self.request.user).get(pk=self.kwargs["pk"]).versions.all()


class ReplyViewSet(ModelViewSet):
    permission_classes = [HasNotRepliedAlready & (IsStaffOrReadOnly | IsRelatedToReviewObjectOrReadOnly)]
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
