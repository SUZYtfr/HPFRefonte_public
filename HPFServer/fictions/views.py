from django.utils import timezone
from django.db.models import Q, F
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from rest_framework import viewsets, response, decorators, exceptions, mixins, permissions

from users.models import UserPreferences
from reviews.utils import can_post_reviews, can_see_reviews
from .enums import ChapterValidationStage


from .models import Fiction, Chapter
from .serializers import (
    FictionSerializer,
    # FictionExtraAuthorSerializer,
    ChapterSerializer,
    # ChapterCardSerializer,
    FictionChapterOrderSerializer,
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
from .filters import DjangoFilterBackend, FictionFilterSet
from reviews.serializers import (
    ChapterReviewSerializer,
    ChapterAnonymousReviewSerializer,
    FictionReviewSerializer,
    FictionAnonymousReviewSerializer,
)

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


class FictionViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    """Ensemble de vues pour les fictions"""
    queryset = Fiction.objects.with_averages().order_by("-creation_date")
    # queryset = Fiction.objects.order_by("-creation_date")
    serializer_class = FictionSerializer
    permission_classes = [IsAuthenticated & (IsCreationUser | IsFictionCoAuthor) | ReadOnly]
    filter_backends = [DjangoFilterBackend]
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

    # @decorators.action(
    #     detail=True,
    #     methods=["POST"],
    #     url_path="anonymous-review",
    #     serializer_class=FictionAnonymousReviewSerializer,
    #     permission_classes=[permissions.AllowAny],
    # )
    # def create_anonymous_review(self, request, *args, **kwargs):
    #     fiction = self.get_object()
    #     if not can_post_reviews(fiction, request.user):
    #         raise
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(fiction=fiction)
    #     return response.Response(data=serializer.validated_data)

    # @decorators.action(
    #     detail=True,
    #     methods=["GET", "PUT"],
    #     url_name="authors",
    #     url_path="authors",
    #     name="Ajouter un co-auteur",
    #     serializer_class=FictionExtraAuthorSerializer,
    #     permission_classes=[IsCreationUser],
    # )
    # def manage_authors(self, request, pk, **kwargs):
    #     """Ajoute """

    #     fiction = self.get_object()

    #     if self.request.method == "PUT":
    #         if self.request.user != fiction.authors.first():
    #             return self.permission_denied(
    #                 request,
    #                 message="Seul l'auteur principal peut ajouter des co-auteurs."
    #             )

    #         serializer = self.serializer_class(instance=fiction, data=request.data)
    #         serializer.is_valid(raise_exception=True)

    #         serializer.save(
    #             modification_user=self.request.user,
    #             modification_time=timezone.now(),
    #         )

    #     return self.retrieve(request)

    @decorators.action(
        detail=True,
        methods=["GET", "PUT"],
        url_name="chapter-order",
        serializer_class=FictionChapterOrderSerializer,
    )
    def order(self, request, *args, **kwargs):
        if request.method == "GET":
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return response.Response(serializer.data)

        elif request.method == "PUT":
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.reorder()

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return response.Response(serializer.data)


class ChapterViewSet(viewsets.ModelViewSet):
    """Ensemble de vues publiques pour les chapitres"""

    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticated & (IsParentFictionCreationUser | IsParentFictionCoAuthor) | ReadOnly]

    def get_queryset(self):
        """Détermine la liste des chapitres à afficher."""

        queryset = super().get_queryset()

        if self.request.user.has_perm("fictions.view_chapter"):
            return queryset.exclude(validation_status=Chapter.ValidationStage.DRAFT)
        elif self.request.query_params.get("self"):
            return queryset.filter(creation_user_id=self.request.user.id)
        else:
            return queryset.filter(validation_status=Chapter.ValidationStage.PUBLISHED)

        # base_queryset = Chapter.objects.filter(fiction_id=self.kwargs["fiction_pk"])

        # if self.request.query_params.get("mine", False) == "True":
        #     return base_queryset.filter(creation_user=self.request.user.id)
        # elif self.kwargs.pop("mine", False):
        #     return base_queryset.filter(creation_user=self.request.user.id)
        # elif self.request.user.has_perm("fictions.view_chapter"):
        #     return base_queryset.exclude(validation_status=Chapter.ValidationStage.DRAFT)
        # else:
        #     return base_queryset.filter(validation_status=Chapter.ValidationStage.PUBLISHED)

    def get_object(self):
        """Renvoie le chapitre correspondant à l'ordre, incrémente son compte de lectures."""

        chapter = super().get_object()

        # https://docs.djangoproject.com/en/4.0/ref/models/expressions/#avoiding-race-conditions-using-f
        if all([
            self.action == "retrieve",
            self.request.user != chapter.fiction.creation_user,
            self.request.user not in chapter.fiction.coauthors.all(),
            chapter.validation_status == ChapterValidationStage.PUBLISHED,
        ]):
            chapter.read_count = F("read_count") + 1
            chapter.save_base()
            chapter.refresh_from_db(fields=["read_count"])

        return chapter

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur."""

        # if self.action == "list":
        #     return ChapterCardSerializer
        return self.serializer_class

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

    def initialize_request(self, request, *args, **kwargs):
        """Force la requête à écrire les fichiers téléchargés dans un fichier temporaire."""

        request = super().initialize_request(request, *args, **kwargs)
        request.upload_handlers = [TemporaryFileUploadHandler(request=request)]
        return request

    @decorators.action(
        detail=True,
        methods=["GET", "POST"],
        url_path="reviews",
        serializer_class=ChapterReviewSerializer,
        permission_classes=[(IsAuthenticated & AuthorPreferenceAllowsMemberReviews) | ReadOnly],
    )
    def manage_reviews(self, request, *args, **kwargs):
        chapter = self.get_object()
        if request.method == "POST":
            if not can_post_reviews(chapter, request.user):
                raise
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(creation_user=self.request.user, chapter=chapter)
            return response.Response(data=serializer.validated_data)
        else:
            reviews = chapter.reviews.published() if can_see_reviews(chapter, request.user) else chapter.reviews.none()
            paginated_reviews = self.paginate_queryset(reviews)
            serializer = self.get_serializer(paginated_reviews, many=True)
            return response.Response(data=serializer.data)

    @decorators.action(
        detail=True,
        methods=["POST"],
        url_path="anonymous-review",
        serializer_class=ChapterAnonymousReviewSerializer,
        permission_classes=[permissions.AllowAny & AuthorPreferenceAllowsAnonymousReviews],
    )
    def create_anonymous_review(self, request, *args, **kwargs):
        chapter = self.get_object()
        if not can_post_reviews(chapter, request.user):
            raise
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(creation_user=self.request.user, chapter=chapter)
        return response.Response(data=serializer.validated_data)

    @decorators.action(
        detail=True,
        methods=["PUT"],
        url_path="submit",
        name="Envoyer",
        # permission_classes=[IsCreationUser | IsParenT],
    )
    def submit(self, request, pk, **kwargs):
        """Envoie le chapitre à la modération"""

        chapter = Chapter.objects.get(pk=pk)

        try:
            chapter.submit()
        except Chapter.InvalidChapterAction as e:
            raise exceptions.APIException(detail=e.message)

        return self.retrieve(request)

    @decorators.action(
        detail=True,
        methods=["PUT"],
        url_path="validate",
        name="Valider",
        permission_classes=[HasStaffValidation],
    )
    def validate(self, request, pk, **kwargs):
        """Valide le chapitre"""

        chapter = Chapter.objects.get(pk=pk)

        try:
            chapter.validate()
        except Chapter.InvalidChapterAction as e:
            raise exceptions.APIException(detail=e.message)

        return self.retrieve(request)

    @decorators.action(
        methods=["PUT"],
        detail=True,
        url_path="invalidate",
        name="Invalider",
        permission_classes=[HasStaffValidation],
    )
    def invalidate(self, request, pk, **kwargs):
        """Invalide le chapitre"""

        chapter = Chapter.objects.get(pk=pk)
        try:
            chapter.invalidate()
        except Chapter.InvalidChapterAction as e:
            raise exceptions.APIException(detail=e.message)

        return self.retrieve(request)


# class CollectionViewSet(viewsets.ModelViewSet):
#     """Ensemble de vues pour les séries"""

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsObjectAuthorOrReadOnly]
#     serializer_class = CollectionSerializer
#     queryset = Collection.objects.order_by("-creation_date")
#     search_fields = ["title", "fictions__title", "summary", "fictions__summary"]

#     def perform_create(self, serializer):
#         serializer.save(creation_user=self.request.user)

#     def perform_update(self, serializer):
#         serializer.save(modification_user=self.request.user)

#     def perform_destroy(self, instance):
#         """Finalise le retrait de l'autorat du membre authentifié sur la série, la supprime si plus aucun autorat"""

#         instance.authors.remove(self.request.user)
#         if instance.authors.count() <= 0:
#             instance.delete()

#     @decorators.action(
#         detail=True,
#         url_path="fictions",
#         url_name="fictions",
#         methods=["GET"],
#         serializer_class=FictionCardSerializer,
#     )
#     def get_fictions(self, request, *args, **kwargs):
#         collection = self.get_object()
#         fictions = collection.fictions.all()
#         paginated_fictions = self.paginate_queryset(fictions)
#         serializer = self.get_serializer(instance=paginated_fictions, many=True)
#         return response.Response(data=serializer.data)

#     @decorators.action(
#         detail=True,
#         methods=["GET", "POST"],
#         url_path="reviews",
#         serializer_class=CollectionReviewSerializer,
#         permission_classes=[IsAuthenticated | ReadOnly],
#     )
#     def manage_reviews(self, request, *args, **kwargs):
#         collection = self.get_object()
#         if request.method == "POST":
#             if not can_post_reviews(collection, request.user):
#                 raise
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save(creation_user=self.request.user, fiction=collection)
#             return response.Response(data=serializer.validated_data)
#         else:
#             reviews = collection.published_reviews.all() if can_see_reviews(collection, request.user) else collection.reviews.none()
#             paginated_reviews = self.paginate_queryset(reviews)
#             serializer = self.get_serializer(paginated_reviews, many=True)
#             return response.Response(data=serializer.data)

#     @decorators.action(
#         detail=True,
#         methods=["POST"],
#         url_path="anonymous-review",
#         serializer_class=CollectionAnonymousReviewSerializer,
#         permission_classes=[permissions.AllowAny],
#     )
#     def create_anonymous_review(self, request, *args, **kwargs):
#         collection = self.get_object()
#         if not can_post_reviews(collection, request.user):
#             raise
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(collection=collection)
#         return response.Response(data=serializer.validated_data)

#     @decorators.action(
#         methods=["GET", "PUT"],
#         detail=True,
#         serializer_class=CollectionChapterOrderSerializer,
#         url_name="chapter-order",
#     )
#     def order(self, request, *args, **kwargs):
#         if request.method == "GET":
#             instance = self.get_object()
#             serializer = self.get_serializer(instance)
#             return response.Response(serializer.data)

#         elif request.method == "PUT":
#             partial = kwargs.pop('partial', False)
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=partial)
#             serializer.is_valid(raise_exception=True)
#             serializer.reorder()

#             if getattr(instance, '_prefetched_objects_cache', None):
#                 # If 'prefetch_related' has been applied to a queryset, we need to
#                 # forcibly invalidate the prefetch cache on the instance.
#                 instance._prefetched_objects_cache = {}

#             return response.Response(serializer.data)
