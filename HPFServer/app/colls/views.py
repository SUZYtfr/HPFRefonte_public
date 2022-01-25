from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CollectionCardSerializer, CollectionSerializer, \
                         MyCollectionCardSerializer, MyCollectionSerializer, CollectionChapterOrderSerializer

from .models import Collection


# VUES PUBLIQUES

class PublicCollectionViewSet(ReadOnlyModelViewSet):
    """Ensemble de vues publiques pour les séries"""

    lookup_url_kwarg = "collection_id"
    serializer_class = CollectionSerializer

    def get_queryset(self):
        """Détermine la liste de séries à afficher"""

        return Collection.objects.all()

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return CollectionCardSerializer

        return self.serializer_class

    @action(methods=["GET", "PUT"], detail=True, serializer_class=CollectionChapterOrderSerializer,
            url_name="chapter-order")
    def order(self, request, *args, **kwargs):
        if request.method == "GET":
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

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

            return Response(serializer.data)


# VUES PRIVÉES

class MyCollectionViewSet(ModelViewSet):
    """Ensemble de vues privées pour les séries"""

    permission_classes = (IsAuthenticated,)
    serializer_class = MyCollectionSerializer

    def get_queryset(self):
        """Détermine la liste de séries du membre authentifié à afficher"""

        return Collection.objects.filter(authors__id=self.request.user.id)

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return MyCollectionCardSerializer

        return self.serializer_class

    def perform_destroy(self, instance):
        """Finalise le retrait de l'autorat du membre authentifié sur la série, la supprime si plus aucun autorat"""

        instance.authors.remove(self.request.user)
        if instance.authors.count() <= 0:
            instance.delete()
