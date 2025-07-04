from django.conf import settings
from django.db import models
from django.utils import timezone
from ordered_model import models as ordered_models
from django.db.models import Manager
from core.models import (
    DatedModel,
    CreatedModel,
    AuthoredModel,
    CharacteristicModel,
    TextDependentModel,
    BaseTextVersionModel,
)
from fictions.enums import (
    FictionStatus,
    ChapterValidationStage,
    CollectionAccess,
)
from images.models import ContentImage


class FictionQuerySet(models.QuerySet):
    def published(self):
        """Retourne les fictions publiées, dont au moins un des chapitres est publié"""

        return self.filter(chapters__published_version__isnull=False).distinct()

    def with_averages(self):
        """Ajoute le total des moyennes des reviews publiées"""

        average = models.Sum(
            "reviews__grading",
            filter=models.Q(reviews__is_draft=False),
        ) / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(_average=average)

    def with_read_counts(self):
        """Ajoute le total des comptes de lectures des chapitres publiés"""

        read_count = models.Sum(
            "chapters__read_count",
            filter=models.Q(chapters__validation_status=ChapterValidationStage.PUBLISHED)
        )
        return self.annotate(_read_count=read_count)

    def with_word_counts(self):
        """Ajoute le total des comptes de mots des chapitres publiés"""

        grouped_published_chapters = Chapter.objects.published().with_word_counts().filter(
            fiction_id=models.OuterRef("id"),
        ).values("fiction_id")

        summed_up_word_counts = grouped_published_chapters.annotate(
            word_count=models.Sum("_word_count"),
        ).values("word_count")

        fictions_with_word_counts = self.annotate(
            _word_count=models.Subquery(summed_up_word_counts),
        )

        return fictions_with_word_counts

    def with_review_counts(self):
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
        ordering = ["-creation_date"]

    title = models.CharField(
        verbose_name="titre",
        max_length=200,
        blank=False,
    )
    summary = models.TextField(
        verbose_name="résumé",
        null=False,
        blank=True,
        default="",
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

    def __str__(self):
        return self.title

    @property
    def published_chapters(self):
        """Renvoie les chapitres publiés"""
        return self.chapters.filter(published_version__isnull=False)
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

        return getattr(self, "_word_count", None) or (
            self.published_chapters
            .with_word_counts()
            .aggregate(word_count=models.Sum("_word_count"))
        )["word_count"]
    word_count.fget.short_description = "compte de mots"

    @property
    def read_count(self) -> int:
        """Renvoie le compte de lectures des chapitres publiés"""

        return getattr(self, "_read_count", None) or sum(
            self.published_chapters
            .filter(read_count__isnull=False)
            .values_list("read_count", flat=True)
        )
    read_count.fget.short_description = "compte de lectures"

    @property
    def published_reviews(self):
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

    def first_chapter(self):
        return self.published_chapters.first()

    def delete(self, using=None, keep_parents=False):
        """Supprime la fiction

            Supprime tous les chapitres de la fiction. Si la fiction persiste, la supprime."""

        for chapter in self.chapters.all():
            chapter.delete()
        if self.id:
            super().delete(using, keep_parents)

    # TODO - sera remplacé par un M2M pour le co-autorat
    @property
    def authors(self) -> list:
        return [self.creation_user]

    # TODO - renommer franchement "collections" en "series" ou l'inverse dans le frontend
    @property
    def series(self) -> list:
        return self.collections.all()


class ChapterQuerySet(models.QuerySet):
    def with_word_counts(self) -> "ChapterQuerySet":
        """Ajoute le total des comptes de mots"""

        last_version_word_count = (
            ChapterVersion.objects
            .filter(chapter_id=models.OuterRef("id"))
            .order_by("-id")
            .values("word_count")
        )[:1]

        chapters_with_word_counts = self.annotate(
            _word_count=models.Subquery(last_version_word_count)
        )

        return chapters_with_word_counts

    def with_averages(self) -> "ChapterQuerySet":
        average = models.Sum("reviews__grading") / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(_average=average)

    def published(self) -> "ChapterQuerySet":
        return self.filter(published_version__isnull=False)


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
    published_version = models.ForeignKey(
        verbose_name="version publiée",
        to="fictions.ChapterVersion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )
    read_count = models.PositiveIntegerField(
        verbose_name="compte de lectures",
        default=0,
        editable=True,
    )
    # validation_status = models.SmallIntegerField(
    #     verbose_name="étape de validation",
    #     choices=ChapterValidationStage.choices,
    #     default=ChapterValidationStage.DRAFT,
    # )
    # TODO faire des trigger warnings une table à part
    trigger_warnings = models.ManyToManyField(
        verbose_name="avertissements",
        to="characteristics.Characteristic",
        limit_choices_to={"characteristic_type": settings.TW_CHARTYPE_ID},
        blank=True,
    )

    def __str__(self) -> str:
        if title := self.title:
            return title
        elif last_version_title := getattr(self.last_version, "title", None):
            return f"{last_version_title} (non publié)"
        else:
            return "Sans titre"  # ne devrait jamais arriver

    def order(self) -> int:
        return self._order + 1

    @property
    def is_published(self) -> bool:
        return bool(self.published_version)
    is_published.fget.short_description = "est publié"
    
    @property
    def title(self) -> str | None:
        return self.published_version.title if self.published_version else None
    title.fget.short_description = "titre"

    @property
    def text(self) -> str | None:
        return self.published_version.text if self.published_version else None
    text.fget.short_description = "texte"

    @property
    def start_note(self) -> str | None:
        return self.published_version.start_note if self.published_version else None
    start_note.fget.short_description = "note de début"
    
    @property
    def end_note(self) -> str | None:
        return self.published_version.end_note if self.published_version else None
    end_note.fget.short_description = "note de fin"
    
    @property
    def word_count(self) -> int | None:
        return self.published_version.word_count if self.published_version else None
    end_note.fget.word_count = "compte de mots"

    @property
    def text_images(self) -> Manager[ContentImage] | None:
        return self.published_version.text_images.all() if self.published_version else None
    text_images.fget.short_description = "images incluses"

    @property
    def last_version(self) -> "ChapterVersion":
        return self.versions.last()  # TODO latest

    # TODO - sera remplacé par un M2M pour le co-autorat
    @property
    def authors(self) -> list:
        return [self.creation_user]

    @property
    def published_reviews(self):
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
    """Modèle de contenu de chapitre"""
    
    class Meta:
        verbose_name = "version de contenu de chapitre"
        verbose_name_plural = "versions de contenu de chapitre"

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
    is_draft = models.BooleanField(
        verbose_name="brouillon",
        default=True,
    )

    text_images = models.ManyToManyField(
        to="images.ContentImage",
        related_name="chapter_text_images",
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
        # et draft dans tout ça?
        if self.is_draft:
            return ChapterValidationStage.DRAFT
        elif self.is_published:
            return ChapterValidationStage.PUBLISHED
        elif self.to_be_discussed:
            return ChapterValidationStage.DISCUTED
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

    def __str__(self):
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
    def published_reviews(self):
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
