from django.conf import settings
from django.db import models
from ordered_model import models as ordered_models
from core.models import (
    DatedModel,
    CreatedModel,
    CharacteristicModel,
    TextDependentModel,
)
from fictions.enums import (
    FictionStatus,
    ChapterValidationStage,
    CollectionAccess,
    Rating,
)
from characteristics.models import TriggerWarning
# from images.models import ContentImage

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from reviews.models import FictionReview, ChapterReview, CollectionReview


class FictionQuerySet(models.QuerySet):
    def published(self) -> models.QuerySet["Fiction"]:
        """Retourne les fictions publiées, dont au moins un des chapitres est publié"""

        return self.filter(chapters__publication_date__isnull=False).distinct()

    def with_averages(self) -> models.QuerySet["Fiction"]:
        """Ajoute le total des moyennes des reviews publiées"""

        average = models.Sum(
            "reviews__grading",
            filter=models.Q(reviews__is_draft=False),
        ) / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(_average=average)

    def with_read_counts(self) -> models.QuerySet["Fiction"]:
        """Ajoute le total des comptes de lectures des chapitres publiés"""

        read_count = models.Sum(
            "chapters__read_count",
            filter=models.Q(chapters__publication_date__isnull=False),
        )
        return self.annotate(_read_count=read_count)

    def with_word_counts(self) -> models.QuerySet["Fiction"]:
        """Ajoute le total des comptes de mots des chapitres publiés"""

        word_count = models.Sum(
            "chapters__word_count",
            filter=models.Q(chapters__publication_date__isnull=False),
        )
        return self.annotate(_word_count=word_count)

    def with_review_counts(self) -> models.QuerySet["Fiction"]:
        """Ajoute le total des reviews publiées"""

        review_count = models.Count(
            "reviews",
            distinct=True,
            filter=models.Q(reviews__is_draft=False),
        )

        return self.annotate(
            _review_count=review_count,
        )


class Fiction(DatedModel, CreatedModel, CharacteristicModel):
    """Modèle de fiction"""

    objects = FictionQuerySet.as_manager()

    class Meta:
        verbose_name = "fiction"
        ordering = ["-last_update_date"]

    title = models.CharField(
        verbose_name="titre",
        max_length=200,
    )
    summary = models.TextField(
        verbose_name="résumé",
    )
    storynote = models.TextField(
        verbose_name="note de fiction",
        null=False,
        blank=True,
        default="",
    )
    status = models.SmallIntegerField(
        verbose_name="état d'écriture",
        choices=FictionStatus.choices,
        default=FictionStatus.PROGRESS,
    )
    is_watched = models.BooleanField(
        default=False,
    )
    featured = models.BooleanField(
        verbose_name="mise en avant",
        default=False,
    )
    last_update_date = models.DateTimeField(
        verbose_name="dernière mise à jour",
        null=True,
        blank=True,
    )

    # coauthors = models.ManyToManyField(
    #     verbose_name="co-auteurs",
    #     to="users.User",
    #     related_name="coauthored_fictions",
    #     blank=True,
    # )

    summary_images = models.ManyToManyField(
        to="images.ContentImage",
        related_name="fiction_summaries",
    )

    fandoms = models.ManyToManyField(
        to="fictions.Fandom",
        related_name="fictions",
    )
    rating = models.PositiveSmallIntegerField(
        verbose_name="audience",
        choices=Rating.choices,
    )

    def __str__(self) -> str:
        return self.title

    @property
    def published_chapters(self) -> models.QuerySet["Chapter"]:
        """Renvoie les chapitres publiés"""
        return self.chapters.filter(publication_date__isnull=False)
    published_chapters.fget.short_description = "chapitres publiés"

    @property
    def is_published(self) -> bool:
        """Détermine si la fiction est publiée, c'est-à-dire si elle a au moins un chapitre publié"""

        return self.published_chapters.exists()
    is_published.fget.short_description = "publiée"

    @property
    def chapter_count(self) -> int:
        """Renvoie le compte de chapitres publiés"""

        return getattr(self, "_chapter_count", None) or self.published_chapters.count()
    chapter_count.fget.short_description = "compte de chapitres"

    @property
    def collection_count(self) -> int:
        """Renvoie le compte de séries"""

        return self.collections.count()
    collection_count.fget.short_description = "compte de séries"

    @property
    def word_count(self) -> int:
        """Renvoie le compte de mots des chapitres publiés"""

        return getattr(self, "_word_count", None) or sum(
            self.published_chapters
            .filter(word_count__isnull=False)
            .values_list("word_count", flat=True),
        )
    word_count.fget.short_description = "compte de mots"

    @property
    def read_count(self) -> int:
        """Renvoie le compte de lectures des chapitres publiés"""

        return getattr(self, "_read_count", None) or sum(
            self.published_chapters
            .filter(read_count__isnull=False)
            .values_list("read_count", flat=True),
        )
    read_count.fget.short_description = "compte de lectures"

    @property
    def published_reviews(self) -> models.QuerySet["FictionReview"]:
        return self.reviews.filter(is_draft=False)
    published_reviews.fget.short_description = "reviews publiées"

    @property
    def average(self) -> float | None:
        """Renvoie la moyenne des reviews"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        return getattr(self, "_average", None) or (sum(filter(None, all_gradings)) / len(all_gradings)) if all_gradings else None

        # if all_gradings:  # pour éviter une division par 0
        #     return sum(filter(None, all_gradings)) / len(all_gradings)
        # else:
        #     return None
    average.fget.short_description = "moyenne"

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews"""

        return getattr(self, "_review_count", None) or self.published_reviews.count()
    review_count.fget.short_description = "compte de reviews"

    def first_chapter(self) -> "Chapter":
        return self.published_chapters.first()

    def delete(self, *args, **kwargs) -> None:
        """Supprime la fiction

            Supprime tous les chapitres de la fiction. Si la fiction persiste, la supprime."""

        for chapter in self.chapters.all():
            chapter.delete()
        if self.id:
            super().delete(*args, **kwargs)

    # TODO - sera remplacé par un M2M pour le co-autorat
    @property
    def authors(self) -> list:
        return [self.creation_user]

    # TODO - renommer franchement "collections" en "series" ou l'inverse dans le frontend
    @property
    def series(self) -> list:
        return self.collections.all()

    @property
    def trigger_warnings(self) -> models.QuerySet["TriggerWarning"]:
        return TriggerWarning.objects.filter(chapter__fiction=self)


class ChapterQuerySet(models.QuerySet):
    def with_averages(self) -> "ChapterQuerySet":
        average = models.Sum("reviews__grading") / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(_average=average)

    def published(self) -> "ChapterQuerySet":
        return self.filter(publication_date__isnull=False)


class Chapter(DatedModel, CreatedModel, TextDependentModel):
    """Modèle de chapitre"""

    class Meta:
        verbose_name = "chapitre"
        order_with_respect_to = "fiction"

    objects = ChapterQuerySet.as_manager()

    fiction = models.ForeignKey(
        to=Fiction,
        verbose_name="fiction",
        related_name="chapters",
        on_delete=models.CASCADE,
    )
    published_version = models.OneToOneField(
        verbose_name="version publiée",
        to="fictions.ChapterVersion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    title = models.CharField(
        verbose_name="titre",
        max_length=250,
        blank=False,
    )
    start_note = models.TextField(
        verbose_name="note de début",
        null=False,
        blank=True,
        default="",
    )
    end_note = models.TextField(
        verbose_name="note de fin",
        null=False,
        blank=True,
        default="",
    )
    text = models.TextField(
        verbose_name="texte",
        editable=True,
    )
    text_images = models.ManyToManyField(
        to="images.ContentImage",
        related_name="chapter_text_images",
    )
    word_count = models.PositiveIntegerField(
        editable=True,
        verbose_name="compte de mots",
    )
    trigger_warnings = models.ManyToManyField(
        verbose_name="avertissements",
        to="characteristics.TriggerWarning",
        blank=True,
    )
    read_count = models.PositiveIntegerField(
        verbose_name="compte de lectures",
        default=0,
        editable=True,
    )
    publication_date = models.DateTimeField(
        verbose_name="Horodatage de publication",
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return self.title

    def is_published(self) -> bool:
        return bool(self.publication_date)

    def order(self) -> int:
        return self._order + 1

    # TODO - sera remplacé par un M2M pour le co-autorat
    @property
    def authors(self) -> list:
        return [self.creation_user]

    @property
    def published_reviews(self) -> models.QuerySet["ChapterReview"]:
        return self.reviews.filter(is_draft=False)
    published_reviews.fget.short_description = "reviews publiées"

    @property
    def average(self) -> float | None:
        """Renvoie la moyenne des reviews"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        return getattr(self, "_average", None) or (sum(filter(None, all_gradings)) / len(all_gradings)) if all_gradings else None

        # all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        # if all_gradings:  # pour éviter une division par 0
        #     return sum(filter(None, all_gradings)) / len(all_gradings)
    average.fget.short_description = "moyenne"

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews"""

        return getattr(self, "_review_count", None) or self.published_reviews.count()
    review_count.fget.short_description = "compte de reviews"


class ChapterVersion(models.Model):
    """Modèle de contenu de chapitre soumis"""

    class Meta:
        verbose_name = "version de chapitre"
        verbose_name_plural = "versions de chapitre"

    chapter = models.ForeignKey(
        verbose_name="chapitre",
        editable=True,
        related_name="versions",
        to="fictions.Chapter",
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name="titre",
        max_length=250,
        blank=False,
    )
    start_note = models.TextField(
        verbose_name="note de début",
        null=False,
        blank=False,
        default="",
    )
    end_note = models.TextField(
        verbose_name="note de fin",
        null=False,
        blank=False,
        default="",
    )
    word_count = models.PositiveIntegerField(
        editable=True,
        verbose_name="compte de mots",
    )
    text = models.TextField(
        verbose_name="texte",
        editable=True,
    )
    creation_date = models.DateTimeField(
        verbose_name="création",
        auto_now_add=True,
        editable=True,
    )
    creation_user = models.ForeignKey(
        verbose_name="créateur",
        editable=True,
        related_name="+",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    submission_date = models.DateTimeField(
        verbose_name="date de soumission",
        null=True,
        blank=True,
    )

    text_images = models.ManyToManyField(
        to="images.ContentImage",
        related_name="chapter_version_text_images",
    )

    # Invalidation
    public_comment = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )
    private_comment = models.CharField(
        null=True,
        blank=True,
        max_length=512,
    )
    invalidation_date = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=False,
    )
    invalidation_user = models.ForeignKey(
        to="users.User",
        on_delete=models.PROTECT,
        related_name="+",
        null=True,
        blank="True",
    )
    invalidation_reasons = models.ManyToManyField(
        verbose_name="raisons",
        to="fictions.InvalidationReason",
        related_name="+",
    )
    to_be_discussed = models.BooleanField(
        verbose_name="discussion en cours",
        default=False,
    )

    @property
    def is_published(self) -> bool:
        return self == self.chapter.published_version

    @property
    def is_invalidated(self) -> bool:
        return bool(self.invalidation_date)

    @property
    def validation_status(self) -> ChapterValidationStage:
        if self.is_published:
            return ChapterValidationStage.PUBLISHED
        elif self.to_be_discussed:
            return ChapterValidationStage.DISCUSSED
        elif self.is_invalidated:
            return ChapterValidationStage.EDIT_REQUIRED
        else:
            return ChapterValidationStage.PENDING


class InvalidationReason(models.Model):
    class Meta:
        verbose_name = "Raison d'invalidation"
        verbose_name_plural = "Raisons d'invalidation"

    reason = models.CharField(
        verbose_name="raison",
        max_length=255,
    )

    def __str__(self) -> str:
        return self.reason


class Collection(DatedModel, CreatedModel, CharacteristicModel):
    """Modèle de série"""

    class Meta:
        verbose_name = "série"

    title = models.CharField(
        verbose_name="titre",
        max_length=200,
    )
    summary = models.TextField(
        verbose_name="résumé",
    )
    summary_images = models.ManyToManyField(
        verbose_name="images de résumé",
        to="images.ContentImage",
        related_name="collection_summaries",
    )
    access = models.SmallIntegerField(
        verbose_name="état",
        choices=CollectionAccess.choices,
        default=CollectionAccess.CLOSED,
    )

    def __str__(self) -> str:
        return self.title

    @property
    def published_reviews(self) -> models.QuerySet["CollectionReview"]:
        return self.reviews.filter(is_draft=False)
    published_reviews.fget.short_description = "reviews publiées"

    @property
    def average(self) -> float | None:
        """Renvoie la moyenne des reviews publiées"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        return getattr(self, "_average", None) or (sum(filter(None, all_gradings)) / len(all_gradings)) if all_gradings else None

        # all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        # if all_gradings:  # pour éviter une division par 0
        #     return sum(filter(None, all_gradings)) / len(all_gradings)
        # else:
        #     return None
    average.fget.short_description = "moyenne"

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews publiées"""

        return getattr(self, "_review_count", None) or self.published_reviews.count()
    review_count.fget.short_description = "compte de reviews"


class CollectionItem(ordered_models.OrderedModel):
    """Modèle de série"""

    class Meta(ordered_models.OrderedModel.Meta):
        verbose_name = "série"
        ordering = ["parent", "order"]
        constraints = [
            models.UniqueConstraint(
                name="UQ_fictions_collectionitem_parent_collection",
                fields=["parent", "collection"],
            ),
            models.UniqueConstraint(
                name="UQ_fictions_collectionitem_parent_fiction",
                fields=["parent", "fiction"],
            ),
            models.UniqueConstraint(
                name="UQ_fictions_collectionitem_parent_chapter",
                fields=["parent", "chapter"],
            ),
            models.CheckConstraint(
                name="CK_fictions_collectionitem_unique_item_type",
                check=(
                    models.Q(collection__isnull=False, fiction__isnull=True, chapter__isnull=True) |
                    models.Q(collection__isnull=True, fiction__isnull=False, chapter__isnull=True) |
                    models.Q(collection__isnull=True, fiction__isnull=True, chapter__isnull=False)
                ),
                violation_error_message="Un élément de série doit contenir un et seulement un élément",
            ),
        ]

    parent = models.ForeignKey(
        verbose_name="série parente",
        to=Collection,
        on_delete=models.CASCADE,
        related_name="items",
    )
    collection = models.ForeignKey(
        verbose_name="série",
        to=Collection,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="collection_items",
    )
    fiction = models.ForeignKey(
        to=Fiction,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="collection_items",
    )
    chapter = models.ForeignKey(
        verbose_name="chapitre",
        to=Chapter,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="collection_items",
    )

    order_with_respect_to = "parent"  # NOTE - django-ordered-model nécessite que ce paramètre se trouve sur le modèle et non dans Meta

    def __str__(self) -> str:
        return f"Élément n°{self.position} de la série {str(self.parent)}"

    @property
    def position(self) -> int | None:
        if self.order is not None:
            return self.order + 1
        else:
            return None


class Fandom(models.Model):
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name
