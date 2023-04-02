from rest_framework import permissions, decorators, response, viewsets

from .serializers import CollectionSerializer, CollectionChapterOrderSerializer
from .models import Collection
from core.permissions import IsObjectAuthorOrReadOnly, IsAuthenticated, ReadOnly
from fictions.serializers import FictionCardSerializer
from reviews.serializers import CollectionReviewSerializer, CollectionAnonymousReviewSerializer
from reviews.utils import can_post_reviews, can_see_reviews

import logging
logging.basicConfig(level=logging.DEBUG)


class CollectionViewSet(viewsets.ModelViewSet):
    """Ensemble de vues pour les séries"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsObjectAuthorOrReadOnly]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.order_by("-creation_date")
    search_fields = ["title", "fictions__title", "summary", "fictions__summary"]

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user)

    def perform_destroy(self, instance):
        """Finalise le retrait de l'autorat du membre authentifié sur la série, la supprime si plus aucun autorat"""

        instance.authors.remove(self.request.user)
        if instance.authors.count() <= 0:
            instance.delete()

    @decorators.action(
        detail=True,
        url_path="fictions",
        url_name="fictions",
        methods=["GET"],
        serializer_class=FictionCardSerializer,
    )
    def get_fictions(self, request, *args, **kwargs):
        collection = self.get_object()
        fictions = collection.fictions.all()
        paginated_fictions = self.paginate_queryset(fictions)
        serializer = self.get_serializer(instance=paginated_fictions, many=True)
        return response.Response(data=serializer.data)

    @decorators.action(
        detail=True,
        methods=["GET", "POST"],
        url_path="reviews",
        serializer_class=CollectionReviewSerializer,
        permission_classes=[IsAuthenticated | ReadOnly],
    )
    def manage_reviews(self, request, *args, **kwargs):
        collection = self.get_object()
        if request.method == "POST":
            if not can_post_reviews(collection, request.user):
                raise
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(creation_user=self.request.user, fiction=collection)
            return response.Response(data=serializer.validated_data)
        else:
            reviews = collection.published_reviews.all() if can_see_reviews(collection, request.user) else collection.reviews.none()
            paginated_reviews = self.paginate_queryset(reviews)
            serializer = self.get_serializer(paginated_reviews, many=True)
            return response.Response(data=serializer.data)

    @decorators.action(
        detail=True,
        methods=["POST"],
        url_path="anonymous-review",
        serializer_class=CollectionAnonymousReviewSerializer,
        permission_classes=[permissions.AllowAny],
    )
    def create_anonymous_review(self, request, *args, **kwargs):
        collection = self.get_object()
        if not can_post_reviews(collection, request.user):
            raise
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(collection=collection)
        return response.Response(data=serializer.validated_data)

    @decorators.action(
        methods=["GET", "PUT"],
        detail=True,
        serializer_class=CollectionChapterOrderSerializer,
        url_name="chapter-order",
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
