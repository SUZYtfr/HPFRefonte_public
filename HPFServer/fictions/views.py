from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from core.permissions import HasBetaTurnOrReadOnly

from .serializers import FictionCardSerializer, FictionSerializer, MyFictionCardSerializer, MyFictionSerializer, \
    FictionChapterOrderSerializer, ChapterCardSerializer, ChapterSerializer, MyChapterCardSerializer, \
    MyChapterSerializer, BetaSerializer, BetaActionSerializer
from .models import Fiction, Chapter, Beta


# VUES PUBLIQUES

class FictionViewSet(ReadOnlyModelViewSet):
    """Ensemble de vues publiques pour les fictions"""

    serializer_class = FictionSerializer

    def get_queryset(self):
        """Détermine la liste de fictions à afficher
        Un utilisateur affiche les fictions validées, un modérateur affiche toutes les fictions."""

        if self.request.user.has_perm("fictions.fiction_list_full_view"):
            return Fiction.objects.all()
        else:
            return Fiction.published.all()

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return FictionCardSerializer

        return self.serializer_class


class ChapterViewSet(ReadOnlyModelViewSet):
    """Ensemble de vues publiques pour les chapitres"""

    serializer_class = ChapterSerializer

    def get_queryset(self):
        """Détermine la liste des chapitres à afficher

            Un utilisateur affiche les chapitres validés.
            Un modérateur affiche tous les chapitres sauf les brouillons."""

        if self.request.user.has_perm("chapters.chapter_list_extended_view"):
            return Chapter.objects.exclude(
                validation_status=Chapter.ChapterValidationStage.DRAFT,
            )
        else:
            return Chapter.objects.filter(
                validation_status=Chapter.ChapterValidationStage.PUBLISHED,
            )

    def get_object(self):
        """Renvoie le chapitre correspondant à l'ordre, incrémente le compte de lectures de la fiction"""

        chapter = super().get_object()

        if self.request.user not in chapter.fiction.authors.all():
            chapter.fiction.read_count += 1
            chapter.fiction.save()

        return chapter

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return ChapterCardSerializer

        return self.serializer_class


# VUES PRIVÉES

class MyFictionsViewSet(ModelViewSet):
    """Ensemble de vues privées pour les fictions"""

    permission_classes = (IsAuthenticated,)
    serializer_class = MyFictionSerializer

    def get_queryset(self):
        """Détermine la liste de fictions du membre authentifié à afficher"""

        return Fiction.objects.filter(authors__id=self.request.user.id)

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return MyFictionCardSerializer
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


class MyChapterViewSet(ModelViewSet):
    """Ensemble de vues privées pour les chapitres"""

    permission_classes = (IsAuthenticated,)
    serializer_class = MyChapterSerializer

    def get_queryset(self):
        """Détermine la liste de chapitres du membre authentifier à afficher, selon l'ID fiction récupéré dans l'URL"""

        return Chapter.objects.filter(creation_user_id=self.request.user.id)

    def get_serializer_class(self):
        """Détermine le sérialiseur à utiliser pour l'action demandé par le routeur"""

        if self.action == "list":
            return MyChapterCardSerializer
        return self.serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "create":
            context["fiction"] = get_object_or_404(Fiction, id=self.kwargs["pk"], authors__id=self.request.user.id)
        return context

    def chapter_list(self, request, **kwargs):
        """Renvoie une réponse JSON contenant la liste des chapitres de la fiction dont l'ID est récupéré dans l'URL"""

        chapters = Fiction.objects.get(pk=kwargs["pk"], authors__id=request.user.id).chapters.all()
        return Response(MyChapterCardSerializer(chapters, many=True, context={"request": request}).data)

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