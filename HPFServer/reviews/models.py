from django.db import models
from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings

from core.models import DatedModel, CreatedModel, TextDependentModel

from django.core.validators import MinValueValidator, MaxValueValidator

from texts.models import ReviewTextVersion

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


class Review(DatedModel, CreatedModel, TextDependentModel):
    """Modèle de review"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    work = GenericForeignKey('content_type', 'object_id')

    draft = models.BooleanField(verbose_name="brouillon")
    grading = models.PositiveSmallIntegerField(verbose_name="notation", null=True, blank=True,
                                               validators=[MinValueValidator(limit_value=MIN_GRADING_VALUE),
                                                           MaxValueValidator(limit_value=MAX_GRADING_VALUE),
                                                           ])

    class Meta:
        verbose_name = "review"
        permissions = [
            ("can_post_review_as_staff", "Peut publier une review avec le compte de modération"),
            ("extra_review_drafts", "Peut sauvegarder plus de brouillons de reviews")
        ]

    @property
    def with_scale(self):
        """Renvoie la notation suivie de la mesure de notation"""

        return f"{str(self.grading or '-')}/10"

    def __str__(self):
        return self.with_scale

    def create_text_version(self, creation_user, text, touch=True):
        """Crée une nouvelle version du texte de review par l'utilisateur passé"""

        version = ReviewTextVersion.objects.create(
            review=self,
            text=text,
            creation_user=creation_user,
            creation_time=timezone.now(),
        )
        version.save()

        if touch:  # à utiliser en cas de modification
            self.save()


class ReviewReply(DatedModel, CreatedModel):
    """Modèle de réponse à review"""

    review = models.ForeignKey(verbose_name="review", related_name="replies",
                               to=Review, null=True, on_delete=models.CASCADE,
                               editable=False)
    parent = models.ForeignKey(verbose_name="parent", to="self", null=True,
                               related_name="replies", on_delete=models.CASCADE,
                               editable=False)
    text = models.TextField(verbose_name="texte", blank=False)

    class Meta:
        verbose_name = "réponse à review"
        verbose_name_plural = "réponses à reviews"

    def __str__(self):
        return self.text[:50]
