from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, permissions

from core.permissions import HasBetaTurnOrReadOnly, IsObjectAuthorOrReadOnly

from .serializers import *
from .models import Fiction, Chapter, Beta


class IsParentFictionAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user in get_object_or_404(Fiction, pk=view.kwargs["pk"]).authors.all():  # TODO - beurk
            return True


class FictionViewSet(ModelViewSet):
    """Ensemble de vues pour les fictions"""

    serializer_class = FictionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsObjectAuthorOrReadOnly]

    def get_queryset(self):
        """Détermine la liste de fictions à afficher."""

        if self.request.query_params.get("mine", False) == "True":
            return Fiction.objects.filter(authors__id=self.request.user.id)
        elif self.request.user.has_perm("fictions.fiction_list_full_view"):
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

    lookup_url_kwarg = "chapter_pk"
    serializer_class = ChapterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsParentFictionAuthorOrReadOnly]

    def get_parent_fiction(self):
        """Récupère la fiction parente depuis l'ID indiqué dans l'URL."""

        return get_object_or_404(Fiction, pk=self.kwargs["pk"])

    def get_queryset(self):
        """Détermine la liste des chapitres à afficher."""

        parent_fiction = self.get_parent_fiction()

        if self.request.query_params.get("mine", False) == "True":
            return parent_fiction.chapters.filter(creation_user_id=self.request.user.id)
        elif self.kwargs.pop("mine", False):
            return parent_fiction.chapters.filter(creation_user_id=self.request.user.id)
        elif self.request.user.has_perm("chapters.chapter_list_extended_view"):
            return parent_fiction.chapters.exclude(validation_status=Chapter.ChapterValidationStage.DRAFT)
        else:
            return parent_fiction.chapters.filter(validation_status=Chapter.ChapterValidationStage.PUBLISHED)

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

    def get_serializer_context(self):
        """Ajoute la fiction parente au contexte passé au sérialiseur."""

        parent_fiction = self.get_parent_fiction()
        context = super().get_serializer_context()
        if self.action == "create":
            context["fiction"] = parent_fiction
        return context

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

    permission_classes = (permissions.IsAuthenticated, HasBetaTurnOrReadOnly,)
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