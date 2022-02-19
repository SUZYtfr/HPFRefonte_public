from django.db import models
from django.utils import timezone

from app.settings import AUTH_USER_MODEL
from core.models import DatedModel, CreatedModel, AuthoredModel, FeaturedModel, ReviewableModel, TextDependentModel, \
    FullCleanModel
from core.text_functions import parse_text, count_words
from texts.models import ChapterTextVersion


class PublishedFictionManager(models.Manager):
    """Gestionnaire de fictions validées"""

    def get_queryset(self):
        return super().get_queryset().filter(chapters__validation_status=7).distinct()


class FictionManager(models.Manager):
    """Gestionnaire de fictions"""

    def create(self, creation_user, title: str, **extra_fields):
        """Crée une fiction, la sauvegarde, crée son autorat, et la renvoie"""

        fiction = self.model(
            title=title,
            creation_user=creation_user,
            **extra_fields
        )

        fiction.save()

        # Sauvegarde > ID Fiction > Possibilité d'assignation d'autorat
        fiction.authors.add(creation_user)

        return fiction


class Fiction(DatedModel, CreatedModel, AuthoredModel, FeaturedModel, ReviewableModel):
    """Modèle de fiction"""

    class FictionStatus(models.IntegerChoices):
        PROGRESS = (1, "En cours")
        PAUSED = (2, "À l'arrêt")
        ABANDONED = (3, "Abandonnée")
        COMPLETED = (4, "Terminée")

    title = models.CharField(verbose_name="titre", max_length=200,
                             blank=False)
    summary = models.TextField(verbose_name="résumé",
                               null=False, blank=True, default="")
    storynote = models.TextField(verbose_name="note de fiction",
                                 null=False, blank=True, default="")
    status = models.SmallIntegerField(verbose_name="état d'écriture",
                                      choices=FictionStatus.choices,
                                      default=FictionStatus.PROGRESS)
    featured = models.BooleanField(verbose_name="mise en avant",
                                   default=False)

    last_update_date = models.DateTimeField(verbose_name="dernière mise à jour",
                                            null=True, blank=True)

    objects = FictionManager()
    published = PublishedFictionManager()

    def __str__(self):
        return self.title

    @property
    def word_count(self):
        """Renvoie la somme des comptes de mots des chapitres publiés"""

        return sum([chapter.word_count for chapter in self.chapters.filter(validation_status=7)])

    @property
    def read_count(self):
        """Renvoie la somme des comptes de lectures des chapitres publiés"""

        return sum([chapter.read_count for chapter in self.chapters.filter(validation_status=7)])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """Supprime la fiction

            Supprime tous les chapitres de la fiction. Si la fiction persiste, la supprime."""

        for chapter in self.chapters.all():
            chapter.delete()
        if self.id:
            super().delete(using, keep_parents)

    @property
    def is_published(self):
        """Détermine si la fiction est publiée, c'est-à-dire si elle a au moins un chapitre publié"""

        return self.chapters.filter(validation_status=7).exists()

    class Meta:
        verbose_name = "fiction"


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

    class ChallengeStatus(models.IntegerChoices):
        OPEN = (1, "Ouvert")
        CLOSED = (2, "Fermé")

    class ChallengeType(models.IntegerChoices):
        CHALLENGE = (1, "Challenge")
        PROJECT = (2, "Projet")

    title = models.CharField(verbose_name="titre", max_length=200,
                             blank=False)
    summary = models.TextField(verbose_name="résumé", blank=False)
    status = models.SmallIntegerField(verbose_name="état", choices=ChallengeStatus.choices)
    challenge_type = models.SmallIntegerField(verbose_name="type", choices=ChallengeType.choices)
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


class Chapter(DatedModel, CreatedModel, ReviewableModel, TextDependentModel):
    """Modèle de chapitre"""

    class Meta:
        verbose_name = "chapitre"
        order_with_respect_to = "fiction"
        permissions = [
            ("automatic_validation", "A la validation automatique des chapitres"),
            ("staff_validation", "A la validation de modérateur des chapitres"),
        ]

    class ChapterValidationStage(models.IntegerChoices):
        DRAFT = (1, "Brouillon")
        BETA_ONGOING = (2, "Bêtatage en cours")
        BETA_COMPLETE = (3, "Bêtatage réalisé")
        PENDING = (4, "En cours de validation")
        EDIT_REQUIRED = (5, "En attente de modification")
        EDITED = (6, "Modifié")
        PUBLISHED = (7, "Publié")

    title = models.CharField(verbose_name="titre", max_length=250,
                             blank=False)
    fiction = models.ForeignKey(to=Fiction,
                                verbose_name="fiction",
                                related_name="chapters",
                                on_delete=models.CASCADE)
    startnote = models.TextField(verbose_name="note de début",
                                 null=False, blank=True, default="")
    endnote = models.TextField(verbose_name="note de fin",
                               null=False, blank=True, default="")
    read_count = models.PositiveIntegerField(default=0, editable=False,
                                             verbose_name="lectures")
    validation_status = models.SmallIntegerField(verbose_name="étape de validation",
                                                 choices=ChapterValidationStage.choices,
                                                 default=ChapterValidationStage.DRAFT)
    poll = models.OneToOneField(verbose_name="sondage",
                                to="polls.PollQuestion",
                                on_delete=models.SET_NULL,
                                null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def word_count(self):
        if version := self.versions.last():
            return version.word_count
        return 0

    def create_text_version(self, creation_user, text, touch=True):
        """Crée une nouvelle version du texte du chapitre par l'utilisateur passé"""

        version = ChapterTextVersion.objects.create(
            chapter=self,
            text=text,
            word_count=count_words(text),
            creation_user=creation_user,
            creation_time=timezone.now(),
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


class Beta(FullCleanModel):
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
