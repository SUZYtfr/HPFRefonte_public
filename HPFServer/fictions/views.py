from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from core.permissions import HasBetaTurnOrReadOnly, IsObjectAuthorOrReadOnly, DjangoPermissionOrReadOnly

from .serializers import *
from .models import Fiction, Chapter, Beta


class IsParentFictionAuthorOReadOnly(DjangoPermissionOrReadOnly):
    """Permission autorisant le contrôle d'un chapitre par l'auteur de sa fiction parente"""

    def has_permission(self, request, view):
        if super(IsParentFictionAuthorOReadOnly, self).has_permission(request, view):
            return True
        elif request.user in get_object_or_404(Fiction, pk=view.kwargs["fiction_pk"]).authors.all():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if super(IsParentFictionAuthorOReadOnly, self).has_object_permission(request, view, obj):
            return True
        elif request.user in obj.fiction.authors.all():
            return True
        return False


class FictionViewSet(ModelViewSet):
    """Ensemble de vues pour les fictions"""

    serializer_class = FictionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectAuthorOrReadOnly]

    def get_queryset(self):
        """Détermine la liste de fictions à afficher."""

        if self.request.query_params.get("mine", False) == "True":
            return Fiction.objects.filter(authors__id=self.request.user.id)
        elif self.request.user.has_perm("fictions.view_fiction"):
            return Fiction.objects.all()
        else:
            return Fiction.published.all()

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return FictionCardSerializer
        return self.serializer_class

    def perform_destroy(self, instance):
        """Finalise le retrait de l'autorat du membre authentifié sur la fiction, la supprime si plus aucun autorat"""

        instance.authors.remove(self.request.user)
        if instance.authors.count() <= 0:
            instance.delete()

    @action(methods=["GET", "PUT"], detail=True, serializer_class=FictionChapterOrderSerializer, url_name="chapter-order")
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


class ChapterViewSet(ModelViewSet):
    """Ensemble de vues publiques pour les chapitres"""

    serializer_class = ChapterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsParentFictionAuthorOReadOnly]

    def get_queryset(self):
        """Détermine la liste des chapitres à afficher."""

        base_queryset = Chapter.objects.filter(fiction_id=self.kwargs["fiction_pk"])

        if self.request.query_params.get("mine", False) == "True":
            return base_queryset.filter(creation_user=self.request.user.id)
        elif self.kwargs.pop("mine", False):
            return base_queryset.filter(creation_user=self.request.user.id)
        elif self.request.user.has_perm("fictions.view_chapter"):
            return base_queryset.exclude(validation_status=Chapter.ChapterValidationStage.DRAFT)
        else:
            return base_queryset.filter(validation_status=Chapter.ChapterValidationStage.PUBLISHED)

    def get_object(self):
        """Renvoie le chapitre correspondant à l'ordre, incrémente le compte de lectures de la fiction"""

        chapter = super().get_object()

        if self.request.user not in chapter.fiction.authors.all():
            chapter.fiction.read_count += 1
            chapter.fiction.save()

        return chapter

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur."""

        if self.action == "list":
            return ChapterCardSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(fiction_id=self.kwargs["fiction_pk"])

    def initialize_request(self, request, *args, **kwargs):
        """Force la requête à écrire les fichiers téléchargés dans un fichier temporaire."""

        request = super().initialize_request(request, *args, **kwargs)
        request.upload_handlers = [TemporaryFileUploadHandler(request=request)]
        return request

    def submit(self, request, **kwargs):

        chapter = self.get_object()

        if request.user.is_premium:
            chapter.validation_status = chapter.ChapterValidationStage.PUBLISHED
            chapter.modification_user = request.user
            chapter.modification_date = timezone.now()
            chapter.save()
            return Response(data="Envoyé", status=status.HTTP_200_OK)
        else:
            if chapter.validation_status in {
                Chapter.ChapterValidationStage.DRAFT,
                Chapter.ChapterValidationStage.BETA_COMPLETE,
                Chapter.ChapterValidationStage.EDITED,
            }:
                chapter.validation_status = chapter.ChapterValidationStage.PENDING
                chapter.modification_user = request.user
                chapter.modification_date = timezone.now()
                chapter.save()
                return Response(data="Envoyé", status=status.HTTP_200_OK)
            else:
                return Response(data="Problème", status=status.HTTP_403_FORBIDDEN)


class BetaViewSet(ModelViewSet):
    """Ensemble de vues pour les bêtatages"""

    permission_classes = (IsAuthenticated, HasBetaTurnOrReadOnly,)
    serializer_class = BetaSerializer

    def get_queryset(self):
        """Renvoie la liste des chapitres sujets à des bêtatages actifs pour l'utilisateur authentifié

            Cette liste contient les chapitres en bêtatages actifs demandés par et à l'utilisateur.
            Exclut les chapitres avec un bêtatage refusé ou clos."""

        return Beta.objects.filter(
            Q(user=self.request.user) |
            Q(chapter__authors=self.request.user)
        ).exclude(
            stage__in=[
                Beta.BetaStage.REFUSED,
                Beta.BetaStage.COMPLETED,
            ]
        )

    def get_serializer_class(self):
        if self.action == "update":
            return BetaActionSerializer

        return self.serializer_class