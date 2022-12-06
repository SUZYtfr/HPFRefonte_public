from django.db import models
from django.utils import timezone

from app.settings import AUTH_USER_MODEL
from core.models import DatedModel, CreatedModel, AuthoredModel, FeaturedModel, TextDependentModel, BaseTextVersionModel
from core.text_functions import count_words


class FictionQuerySet(models.QuerySet):
    def published(self):
        return self.filter(chapters__validation_status=Chapter.ValidationStage.PUBLISHED).distinct()

    def means(self):
        mean = models.Sum("reviews__grading") / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(annotated_mean=mean)

    def read_counts(self):
        read_count = models.Sum(
            "chapters__read_count",
            filter=models.Q(chapters__validation_status=Chapter.ValidationStage.PUBLISHED)
        )
        return self.annotate(read_count=read_count)

    def word_counts(self):
        last_version = ChapterTextVersion.objects.filter(chapter__fiction=models.OuterRef("pk")).order_by("-pk")
        word_count = models.Sum(
            models.Subquery(last_version.values("word_count")[:1]),
            filter=models.Q(chapters__validation_status=Chapter.ValidationStage.PUBLISHED)
        )
        return self.alias(word_count=word_count)


class Fiction(DatedModel, CreatedModel, FeaturedModel):
    """Modèle de fiction"""

    class Status(models.IntegerChoices):
        PROGRESS = (1, "En cours")
        PAUSED = (2, "À l'arrêt")
        ABANDONED = (3, "Abandonnée")
        COMPLETED = (4, "Terminée")

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
        choices=Status.choices,
        default=Status.PROGRESS,
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

    objects = FictionQuerySet.as_manager()

    def __str__(self):
        return self.title

    @property
    def published_chapters(self):
        """Renvoie les chapitres publiés"""
        return self.chapters.filter(validation_status=Chapter.ValidationStage.PUBLISHED)

    @property
    def is_published(self) -> bool:
        """Détermine si la fiction est publiée, c'est-à-dire si elle a au moins un chapitre publié"""

        return self.published_chapters.exists()

    @property
    def chapter_count(self) -> int:
        """Renvoie le compte de chapitres publiés"""

        return self.published_chapters.count()

    @property
    def collection_count(self) -> int:
        """Renvoie le compte de séries"""

        return self.collections.count()

    @property
    def word_count(self) -> int:
        """Renvoie le compte de mots des chapitres publiés"""

        last_version = ChapterTextVersion.objects.filter(chapter=models.OuterRef("pk")).order_by("-pk")
        word_count = models.Subquery(last_version.values('word_count')[:1])
        return sum(
            self.published_chapters
            .annotate(word_count=word_count)
            .filter(word_count__isnull=False)
            .values_list("word_count", flat=True)
        )

    @property
    def read_count(self) -> int:
        """Renvoie le compte de lectures des chapitres publiés"""

        return sum(
            self.published_chapters
            .filter(read_count__isnull=False)
            .values_list("read_count", flat=True)
        )

    @property
    def published_reviews(self):
        return self.reviews.filter(draft=False)

    @property
    def mean(self) -> float:
        """Renvoie la moyenne des reviews"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        if all_gradings:  # pour éviter une division par 0
            return sum(filter(None, all_gradings)) / len(all_gradings)

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews"""
        return self.published_reviews.count()

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
    def word_counts(self):
        last_version = ChapterTextVersion.objects.filter(chapter=models.OuterRef("pk")).order_by("-pk")
        word_count = models.Subquery(last_version.values('word_count')[:1])
        return self.annotate(word_count=word_count)

    def means(self):
        mean = models.Sum("reviews__grading") / models.Count(models.Q(reviews__grading__isnull=False))
        return self.annotate(annotated_mean=mean)

    def published(self):
        return self.filter(validation_status=Chapter.ValidationStage.PUBLISHED)


class Chapter(DatedModel, CreatedModel, TextDependentModel):
    """Modèle de chapitre"""

    class Meta:
        verbose_name = "chapitre"
        order_with_respect_to = "fiction"
        permissions = [
            ("automatic_validation", "A la validation automatique des chapitres"),
            ("staff_validation", "A la validation de modérateur des chapitres"),
        ]

    class ValidationStage(models.IntegerChoices):
        DRAFT = (1, "Brouillon")
        BETA_ONGOING = (2, "Bêtatage en cours")
        BETA_COMPLETE = (3, "Bêtatage réalisé")
        PENDING = (4, "En cours de validation")
        EDIT_REQUIRED = (5, "En attente de modification")
        EDITED = (6, "Modifié")
        PUBLISHED = (7, "Publié")

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
        choices=ValidationStage.choices,
        default=ValidationStage.DRAFT,
    )
    poll = models.OneToOneField(
        verbose_name="sondage",
        to="polls.PollQuestion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = ChapterQuerySet.as_manager()

    def __str__(self):
        return self.title

    @property
    def published_reviews(self):
        return self.reviews.filter(draft=False)

    @property
    def mean(self) -> int:
        """Renvoie la moyenne des reviews"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        if all_gradings:  # pour éviter une division par 0
            return sum(filter(None, all_gradings)) / len(all_gradings)

    @property
    def text(self) -> str:
        return getattr(self.versions.first(), "text", None)

    @property
    def word_count(self) -> int:
        return getattr(self.versions.first(), "word_count")

    @property
    def review_count(self) -> int:
        """Renvoie le nombre de reviews"""
        return self.published_reviews.count()

    def create_text_version(self, creation_user, text, touch=True):
        """Crée une nouvelle version du texte du chapitre par l'utilisateur passé"""

        version = ChapterTextVersion.objects.create(
            chapter=self,
            text=text,
            word_count=count_words(text),
            creation_user=creation_user,
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
        if self.validation_status == Chapter.ValidationStage.DRAFT:
            if self.fiction.creation_user.has_perm("fictions.automatic_validation"):
                self.change_status(
                    Chapter.ValidationStage.PUBLISHED,
                    modification_user=user,
                    modification_time=timezone.now(),
                )

            else:
                self.change_status(
                    Chapter.ValidationStage.PENDING,
                    modification_user=user,
                    modification_time=timezone.now(),
                )

        elif self.validation_status == self.ValidationStage.EDIT_REQUIRED:
            self.change_status(
                Chapter.ValidationStage.EDITED,
                modification_user=user,
                modification_time=timezone.now(),
            )

        else:
            raise Chapter.InvalidChapterAction

    def validate(self, user=None):
        if self.validation_status not in [
            Chapter.ValidationStage.PENDING,
            Chapter.ValidationStage.EDITED,
        ]:
            raise Chapter.InvalidChapterAction

        self.change_status(
            Chapter.ValidationStage.PUBLISHED,
            modification_user=user,
            modification_time=timezone.now(),
        )

    def invalidate(self, user=None):
        if self.validation_status not in [
            Chapter.ValidationStage.PENDING,
            Chapter.ValidationStage.EDITED,
            Chapter.ValidationStage.PUBLISHED,
        ]:
            raise Chapter.InvalidChapterAction

        self.change_status(
            Chapter.ValidationStage.EDIT_REQUIRED,
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


class ChallengeManager(models.Manager):
    """Gestionnaire de challenges"""

    def create(self, title, summary, creation_user,
               **extra_fields):
        if not title:
            raise ValueError("Le titre ne peut pas être laissé vide.")
        if not summary:
            raise ValueError("Le résumé ne peut pas être laissé vide.")

        challenge = self.model(
            title=title,
            summary=summary,
            creation_user=creation_user,
            **extra_fields
        )

        challenge.save()

        # Sauvegarde > ID Challenge > Possibilité d'assignation d'autorat
        challenge.authors.add(creation_user)

        return challenge


class Challenge(DatedModel, CreatedModel, AuthoredModel, FeaturedModel):
    """Modèle de challenge"""

    class Status(models.IntegerChoices):
        OPEN = (1, "Ouvert")
        CLOSED = (2, "Fermé")

    class Type(models.IntegerChoices):
        CHALLENGE = (1, "Challenge")
        PROJECT = (2, "Projet")

    title = models.CharField(verbose_name="titre", max_length=200,
                             blank=False)
    summary = models.TextField(verbose_name="résumé", blank=False)
    status = models.SmallIntegerField(verbose_name="état", choices=Status.choices)
    challenge_type = models.SmallIntegerField(verbose_name="type", choices=Type.choices)
    official = models.BooleanField(verbose_name="officiel", default=False)
    deadline = models.DateTimeField(verbose_name="clôture", null=True)
    forum_link = models.CharField(verbose_name="lien vers le forum", max_length=400,
                                  null=False, blank=True)

    objects = ChallengeManager()

    class Meta:
        verbose_name = "challenge"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.id:
            self.modification_date = timezone.now()
            self.modification_user = kwargs.pop("modification_user", self.modification_user)
        super().save(*args, **kwargs)


class Beta(models.Model):
    """Modèle de bêtatage"""

    class BetaStage(models.IntegerChoices):
        REQUESTED = (1, "Demandé par l'auteur")
        ONGOING = (2, "Accepté par le correcteur")
        REFUSED = (3, "Refusé par le correcteur")
        CORRECTED = (4, "Terminé par le correcteur")
        COMPLETED = (5, "Terminé par l'auteur")

    class Meta:
        verbose_name = "bêtatage"
        constraints = [
            models.UniqueConstraint(
                name="unique_ongoing_beta",
                fields=["chapter"],
                condition=models.Q(stage__in=[1, 2, 4]),
            ),
        ]

    chapter = models.ForeignKey(verbose_name="chapitre", to=Chapter, on_delete=models.CASCADE,
                                related_name="betas")
    user = models.ForeignKey(verbose_name="correcteur", to=AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="betas")
    stage = models.SmallIntegerField(verbose_name="état", choices=BetaStage.choices,
                                     default=BetaStage.REQUESTED)

    def __str__(self):
        return f"{self.chapter} (correcteur : {self.user})"

    @property
    def text(self):
        return self.chapter.text
