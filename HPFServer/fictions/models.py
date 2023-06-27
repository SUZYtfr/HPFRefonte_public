from django.db import models
from django.utils import timezone

from core.models import (
    DatedModel,
    CreatedModel,
    AuthoredModel,
    CharacteristicModel,
    TextDependentModel,
    BaseTextVersionModel,
)
from core.text_functions import count_words
from .enums import (
    FictionStatus,
    ChapterValidationStage,
    CollectionAccess,
)


class FictionQuerySet(models.QuerySet):
    def published(self):
        return self.filter(chapters__validation_status=ChapterValidationStage.PUBLISHED).distinct()

    def with_averages(self):
        average = models.Sum(
            "reviews__grading",
            filter=models.Q(reviews__draft=False),
        ) / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(_average=average)

    def with_read_counts(self):
        read_count = models.Sum(
            "chapters__read_count",
            filter=models.Q(chapters__validation_status=ChapterValidationStage.PUBLISHED)
        )
        return self.annotate(_read_count=read_count)

    def with_word_counts(self):
        """Ajoute le total des comptes de mots des chapitres publiés des fictions"""

        grouped_published_chapters = Chapter.objects.with_word_counts().filter(
            fiction_id=models.OuterRef("id"),
            validation_status=ChapterValidationStage.PUBLISHED,
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
            filter=models.Q(reviews__draft=False),
        )

        return self.annotate(
            _review_count=review_count,
        )


class Fiction(DatedModel, CreatedModel, CharacteristicModel):
    """Modèle de fiction"""

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
    featured = models.BooleanField(
        verbose_name="mise en avant",
        default=False,
    )
    last_update_date = models.DateTimeField(
        verbose_name="dernière mise à jour",
        null=True,
        blank=True,
    )

    coauthors = models.ManyToManyField(
        verbose_name="co-auteurs",
        to="users.User",
        related_name="coauthored_fictions",
    )

    summary_images = models.ManyToManyField(
        to="images.ContentImage",
        related_name="fiction_summaries",
    )

    objects = FictionQuerySet.as_manager()

    def __str__(self):
        return self.title

    @property
    def published_chapters(self):
        """Renvoie les chapitres publiés"""
        return self.chapters.filter(validation_status=ChapterValidationStage.PUBLISHED)

    @property
    def is_published(self) -> bool:
        """Détermine si la fiction est publiée, c'est-à-dire si elle a au moins un chapitre publié"""

        return self.published_chapters.exists()

    @property
    def chapter_count(self) -> int:
        """Renvoie le compte de chapitres publiés"""

        return getattr(self, "_chapter_count", None) or self.published_chapters.count()

    @property
    def collection_count(self) -> int:
        """Renvoie le compte de séries"""

        return self.collections.count()

    @property
    def word_count(self) -> int:
        """Renvoie le compte de mots des chapitres publiés"""

        return getattr(self, "_word_count", None) or (
            self.chapters.
            published().
            with_word_counts().
            aggregate(word_count=models.Sum("_word_count"))
        )["word_count"]

    @property
    def read_count(self) -> int:
        """Renvoie le compte de lectures des chapitres publiés"""

        return getattr(self, "_read_count", None) or sum(
            self.published_chapters
            .filter(read_count__isnull=False)
            .values_list("read_count", flat=True)
        )

    @property
    def published_reviews(self):
        return self.reviews.filter(draft=False)

    @property
    def average(self) -> float | None:
        """Renvoie la moyenne des reviews"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        return getattr(self, "_average", None) or (sum(filter(None, all_gradings)) / len(all_gradings)) if all_gradings else None

        # if all_gradings:  # pour éviter une division par 0
        #     return sum(filter(None, all_gradings)) / len(all_gradings)
        # else:
        #     return None

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews"""

        return getattr(self, "_review_count", None) or self.published_reviews.count()

    def delete(self, using=None, keep_parents=False):
        """Supprime la fiction

            Supprime tous les chapitres de la fiction. Si la fiction persiste, la supprime."""

        for chapter in self.chapters.all():
            chapter.delete()
        if self.id:
            super().delete(using, keep_parents)

    class Meta:
        verbose_name = "fiction"
        ordering = ["-creation_date"]


class ChapterQuerySet(models.QuerySet):
    def with_word_counts(self):

        last_version_word_count = (
            ChapterTextVersion.objects
            .filter(chapter_id=models.OuterRef('id'))
            .order_by('-id')
            .values('word_count')
        )[:1]

        chapters_with_word_counts = Chapter.objects.annotate(
            _word_count=models.Subquery(last_version_word_count)
        )

        return chapters_with_word_counts

    def with_averages(self):
        average = models.Sum("reviews__grading") / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(_average=average)

    def published(self):
        return self.filter(validation_status=ChapterValidationStage.PUBLISHED)


class Chapter(DatedModel, CreatedModel, TextDependentModel):
    """Modèle de chapitre"""

    class Meta:
        verbose_name = "chapitre"
        order_with_respect_to = "fiction"
        permissions = [
            ("automatic_validation", "A la validation automatique des chapitres"),
            ("staff_validation", "A la validation de modérateur des chapitres"),
        ]

    class InvalidChapterAction(Exception):
        message = "Cette action est invalide."

    title = models.CharField(
        verbose_name="titre",
        max_length=250,
        blank=False,
    )
    fiction = models.ForeignKey(
        to=Fiction,
        verbose_name="fiction",
        related_name="chapters",
        on_delete=models.CASCADE,
    )
    startnote = models.TextField(
        verbose_name="note de début",
        null=False,
        blank=True,
        default="",
    )
    endnote = models.TextField(
        verbose_name="note de fin",
        null=False,
        blank=True,
        default="",
    )
    read_count = models.PositiveIntegerField(
        verbose_name="lectures",
        default=0,
        editable=False,
    )
    validation_status = models.SmallIntegerField(
        verbose_name="étape de validation",
        choices=ChapterValidationStage.choices,
        default=ChapterValidationStage.DRAFT,
    )

    text_images = models.ManyToManyField(
        to="images.ContentImage",
        related_name="chapter_text_images",
    )

    objects = ChapterQuerySet.as_manager()

    def __str__(self):
        return self.title

    def order(self) -> int:
        return self._order + 1

    @property
    def published_reviews(self):
        return self.reviews.filter(draft=False)

    @property
    def average(self) -> float | None:
        """Renvoie la moyenne des reviews"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        return getattr(self, "_average", None) or (sum(filter(None, all_gradings)) / len(all_gradings)) if all_gradings else None

        # all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        # if all_gradings:  # pour éviter une division par 0
        #     return sum(filter(None, all_gradings)) / len(all_gradings)

    @property
    def text(self) -> str:
        return getattr(self.versions.first(), "text", "")

    @property
    def word_count(self) -> int:
        return getattr(self, "_word_count", None) or getattr(self.versions.first(), "word_count", None)

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews"""

        return getattr(self, "_review_count", None) or self.published_reviews.count()

    def create_text_version(self, creation_user_id, text, touch=True):
        """Crée une nouvelle version du texte du chapitre par l'utilisateur passé"""

        version = ChapterTextVersion.objects.create(
            chapter=self,
            text=text,
            word_count=count_words(text),
            creation_user_id=creation_user_id,
            creation_date=timezone.now(),
        )
        version.save()

        if touch:  # à utiliser en cas de modification
            self.save()

    def change_status(self, status, modification_user=None, modification_time=None):
        """Change le status de validation du chapitre"""

        self.validation_status = status

        if modification_user:
            self.modification_user = modification_user
            self.modification_date = modification_time or timezone.now()

        self.save()

    def submit(self, user=None):
        if self.validation_status == ChapterValidationStage.DRAFT:
            if self.fiction.creation_user.has_perm("fictions.automatic_validation"):
                self.change_status(
                    ChapterValidationStage.PUBLISHED,
                    modification_user=user,
                    modification_time=timezone.now(),
                )

            else:
                self.change_status(
                    ChapterValidationStage.PENDING,
                    modification_user=user,
                    modification_time=timezone.now(),
                )

        elif self.validation_status == ChapterValidationStage.EDIT_REQUIRED:
            self.change_status(
                ChapterValidationStage.EDITED,
                modification_user=user,
                modification_time=timezone.now(),
            )

        else:
            raise Chapter.InvalidChapterAction

    def validate(self, user=None):
        if self.validation_status not in [
            ChapterValidationStage.PENDING,
            ChapterValidationStage.EDITED,
        ]:
            raise Chapter.InvalidChapterAction

        self.change_status(
            ChapterValidationStage.PUBLISHED,
            modification_user=user,
            modification_time=timezone.now(),
        )

    def invalidate(self, user=None):
        if self.validation_status not in [
            ChapterValidationStage.PENDING,
            ChapterValidationStage.EDITED,
            ChapterValidationStage.PUBLISHED,
        ]:
            raise Chapter.InvalidChapterAction

        self.change_status(
            ChapterValidationStage.EDIT_REQUIRED,
            modification_user=user,
            modification_time=timezone.now(),
        )


class ChapterTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de chapitre"""

    class Meta:
        verbose_name = "version de texte de chapitre"
        verbose_name_plural = "versions de textes de chapitres"

    chapter = models.ForeignKey(
        verbose_name="chapitre",
        editable=False,
        related_name="versions",
        to="fictions.Chapter",
        on_delete=models.CASCADE,
    )
    word_count = models.IntegerField(
        editable=False,
        verbose_name="compte de mots",
    )


class Collection(DatedModel, CreatedModel, AuthoredModel, CharacteristicModel):
    """Modèle de série"""

    title = models.CharField(
        verbose_name="titre",
        max_length=200,
    )
    summary = models.TextField(
        verbose_name="résumé",
    )
    status = models.SmallIntegerField(
        verbose_name="état",
        choices=CollectionAccess.choices,
        default=CollectionAccess.CLOSED,
    )
    parent = models.ForeignKey(
        verbose_name="série parente",
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="subcollections",
    )

    fictions = models.ManyToManyField(
        verbose_name="fictions",
        to="fictions.Fiction",
        # through="FictionCollectionPosition",
        related_name="collections",
    )

    @property
    def published_reviews(self):
        return self.reviews.filter(draft=False)

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

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews publiées"""

        return getattr(self, "_review_count", None) or self.published_reviews.count()

    @property
    def fiction_count(self) -> int:
        """Renvoie le compte de fictions"""

        return getattr(self, "_fiction_count", None) or self.fictions.count()

    class Meta:
        verbose_name = "série"

    def __str__(self):
        return self.title


# class FictionCollectionPosition(OrderedModel):

#     collection = models.ForeignKey(
#         to=Collection,
#         on_delete=models.CASCADE,
#     )
#     fiction = models.ForeignKey(
#         to="fictions.Fiction",
#         on_delete=models.CASCADE,
#     )

#     order_with_respect_to = "collection"

#     class Meta:
#         ordering = ["collection", "order"]
#         constraints = [
#             models.UniqueConstraint(
#                 name="UQ_colls_fictioncollectionposition_collection_fiction",
#                 fields=["collection", "fiction"],
#             ),
#             models.UniqueConstraint(
#                 name="UQ_colls_fictioncollectionposition_collection_order",
#                 fields=["collection", "fiction"],
#             )
#         ]

#     def __repr__(self):
#         return self.collection.title[:15] + " <-> " + self.fiction.title[:15]

#     def __str__(self):
#         return self.__repr__()
