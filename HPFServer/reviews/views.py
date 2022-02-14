from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN

from .models import Review, ReviewReply
from .serializers import ReviewSerializer, AnonymousReviewSerializer, StaffReviewSerializer, \
    ReviewReplySerializer, ReviewCardSerializer, ReviewTextSerializer

from django.db.models import Q
from django.contrib.contenttypes.models import ContentType


class ReviewsListCreateView(ListCreateAPIView):
    """Vue de listage et de création de reviews"""

    serializer_class = ReviewSerializer

    # TODO - fonctionne mais beurk
    def get_queryset(self):
        """Récupère la liste des reviews portant sur le type de contenu passé dans l'URL"""

        return Review.objects.filter(
            draft=False,
            content_type=ContentType.objects.get(model=self.kwargs["contenttype"]).id,
            object_id=self.kwargs["pk"],
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()

        work = ContentType.objects.get(model=self.kwargs["contenttype"]).get_object_for_this_type(pk=self.kwargs["pk"])

        context["work"] = work
        return context

    def get_serializer_class(self):
        """Détermine le sérialiseur selon le rôle de l'utilisateur"""
        if self.request.user.is_anonymous:
            return AnonymousReviewSerializer
        elif self.request.user.has_perm("reviews.can_post_review_as_staff"):
            return StaffReviewSerializer

        return self.serializer_class


class PersonalReviewsListView(ListAPIView):
    """Vue publique de listage des reviews personnelles"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(draft=False, creation_user=self.kwargs["user_id"])


# VUES PRIVÉES

class ReviewsOnMeListView(ModelViewSet):
    """Vue privée de listage des reviews concernant l'auteur et ses œuvres"""

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Renvoie les reviews publiées concernant l'auteur et ses œuvres"""

        return Review.objects.filter(
            Q(user=self.request.user) |
            Q(fiction__authors=self.request.user) |
            Q(chapter__authors=self.request.user) |
            Q(collection__authors=self.request.user),
            draft=False,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ReviewCardSerializer
        elif self.action == "retrieve":
            return ReviewSerializer
        elif self.action == "create":
            return ReviewReplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.action in ["create", "retrieve"]:
            context["review"] = self.get_object()

        return context

    def perform_create(self, serializer):
        """Finalise la création de la réponse à review

        Vérifie le droit de réponse à review de l'utilisateur"""

        try:
            serializer.save()
        except PermissionError as e:
            raise PermissionDenied(
                code=HTTP_403_FORBIDDEN,
                detail=str(e),
            )


class MyPersonalReviewsListView(ModelViewSet):
    """Vue privée de listage des reviews personnelles"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(creation_user=self.request.user)


class MyPersonalReviewHistoryView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewTextSerializer

    def get_queryset(self):
        return Review.objects.filter(creation_user=self.request.user).get(pk=self.kwargs["pk"]).versions.all()


class ReplyViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReviewReplySerializer

    def get_queryset(self):
        return Review.objects.filter(
            pk=self.kwargs["pk"],
            draft=False,
        ).replies.all()

    def get_object(self):
        return ReviewReply.objects.get(pk=self.kwargs["reply_pk"])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if "reply_pk" in self.kwargs.keys():
            context["parent"] = self.get_object()
        else:
            context["parent"] = None
        context["review"] = Review.objects.get(pk=self.kwargs["pk"])
        return context
