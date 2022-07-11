from django.db import models, utils, transaction
from django.utils import timezone
from django.conf import settings
from django.core import validators

from core.models import DatedModel, CreatedModel, TextDependentModel, BaseTextVersionModel
from core.utils import get_moderation_account

from users.models import User
from fictions.models import Fiction, Chapter
from colls.models import Collection

MIN_GRADING_VALUE = 1
MAX_GRADING_VALUE = 10


def check_draft_permission(creation_user):
    """Vérifie la permission de brouillon de l'utilisateur"""

    draft_number = creation_user.created_reviews.filter(draft=True).count()
    if creation_user.has_perm("extra_review_drafts"):
        if draft_number >= settings.PREMIUM_MAX_REVIEW_DRAFTS:
            raise PermissionError("Cet adhérent a atteint son nombre de brouillons de reviews maximal autorisé.")
    else:
        if draft_number >= settings.MEMBERS_MAX_REVIEW_DRAFTS:
            raise PermissionError("Ce membre a atteint son nombre de brouillons de reviews maximal autorisé.")


class ReviewManager(models.Manager):
    @transaction.atomic
    def create(self, creation_user, text, **extra_fields):
        if self.filter(creation_user=creation_user).exists():
            raise utils.IntegrityError
        instance = self.model(creation_user=creation_user, **extra_fields)
        instance.save()
        instance.text = text
        return instance

    def create_anonymous(self, email, **extra_fields):
        creation_user = User.objects.filter(email=email).first()
        if creation_user:
            if creation_user.is_active:
                raise
        else:
            creation_user = User.objects.create_anonymous_user(email, **extra_fields)
        return self.create(creation_user=creation_user, **extra_fields)

    def published(self):
        return self.filter(draft=False)


class Review(DatedModel, CreatedModel, TextDependentModel):
    """Modèle de review"""

    draft = models.BooleanField(
        verbose_name="brouillon",
        default=True,
    )
    grading = models.PositiveSmallIntegerField(
        verbose_name="notation",
        null=True,
        blank=True,
        validators=[
            validators.MinValueValidator(limit_value=MIN_GRADING_VALUE),
            validators.MaxValueValidator(limit_value=MAX_GRADING_VALUE),
        ]
    )

    class Meta:
        permissions = [
            ("can_post_review_as_staff", "Peut publier une review avec le compte de modération"),
            ("extra_review_drafts", "Peut sauvegarder plus de brouillons de reviews")
        ]

    def __str__(self):
        return self.with_scale

    @property
    def reply_count(self):
        return self.replies.count()

    @property
    def with_scale(self):
        """Renvoie la notation suivie de la mesure de notation"""

        return f"{str(self.grading or '-')}/10"

    # def create_text_version(self, creation_user, text, touch=True):
    #     """Crée une nouvelle version du texte de review par l'utilisateur passé"""
    #
    #     version = ReviewTextVersion.objects.create(
    #         review=self,
    #         text=text,
    #         creation_user=creation_user,
    #         creation_date=timezone.now(),
    #     )
    #     version.save()
    #
    #     if touch:  # à utiliser en cas de modification
    #         self.save()

    @property
    def text(self):
        if version := self.versions.first():
            return version.text
        return None

    @text.setter
    def text(self, text):
        if self.text != text:
            version = ReviewTextVersion.objects.create(
                review=self,
                text=text,
                creation_user=self.modification_user or self.creation_user,
            )
            version.save()


class ReviewReply(DatedModel, CreatedModel):
    """Modèle de réponse à review"""

    review = models.ForeignKey(
        verbose_name="review",
        related_name="replies",
        to=Review,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )
    parent = models.ForeignKey(
        verbose_name="parent",
        to="self", null=True,
        related_name="replies",
        on_delete=models.CASCADE,
        editable=False,
    )
    text = models.TextField(
        verbose_name="texte",
        blank=False,
    )

    class Meta:
        verbose_name = "réponse à review"
        verbose_name_plural = "réponses à reviews"

    def __str__(self):
        return self.text[:50]


class FictionReview(Review):
    fiction = models.ForeignKey(
        to=Fiction,
        on_delete=models.CASCADE,
        verbose_name="fiction",
        related_name="reviews",
        editable=False,
    )

    class Meta:
        verbose_name = "review de fiction"
        verbose_name_plural = "reviews de fictions"

    objects = ReviewManager()


class ChapterReview(Review):
    chapter = models.ForeignKey(
        to=Chapter,
        on_delete=models.CASCADE,
        verbose_name="chapitre",
        related_name="reviews",
        editable=False,
    )

    class Meta:
        verbose_name = "review de chapitre"
        verbose_name_plural = "reviews de chapitres"

    objects = ReviewManager()


class CollectionReview(Review):
    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
        verbose_name="série",
        related_name="reviews",
        editable=False,
    )

    class Meta:
        verbose_name = "review de série"
        verbose_name_plural = "reviews de séries"


class ReviewTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de review"""

    class Meta:
        verbose_name = "version de texte de review"
        verbose_name_plural = "versions de textes de reviews"

    review = models.ForeignKey(
        verbose_name="review",
        editable=False,
        related_name="versions",
        to="reviews.Review",
        on_delete=models.CASCADE,
    )

