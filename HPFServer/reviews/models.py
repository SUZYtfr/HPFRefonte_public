from django.db import models
from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from django.conf import settings

from core.models import DatedModel, CreatedModel, TextDependentModel
from core.text_functions import parse_text

from django.core.validators import MinValueValidator, MaxValueValidator

from texts.models import ReviewTextVersion


MIN_GRADING_VALUE = 0
MAX_GRADING_VALUE = 10


def check_review_permission(reviewed_element, creation_user):
    """Vérifie la permission de création de review de l'utilisateur"""

    if hasattr(reviewed_element, "authors") and (creation_user in reviewed_element.authors.all()):
        raise PermissionError("Un auteur ne peut pas créer une review sur sa propre œuvre.")
    elif creation_user == reviewed_element:
        raise PermissionError("Un auteur ne peut pas créer une review sur sa propre personne.")
    elif reviewed_element.reviews.filter(creation_user=creation_user):
        raise PermissionError("Cet utilisateur a déjà créé une review pour cet élément.")


def check_draft_permission(creation_user):
    """Vérifie la permission de brouillon de l'utilisateur"""

    draft_number = creation_user.created_reviews.filter(draft=True).count()
    if creation_user.has_perm("extra_review_drafts"):
        if draft_number >= settings.PREMIUM_MAX_REVIEW_DRAFTS:
            raise PermissionError("Cet adhérent a atteint son nombre de brouillons de reviews maximal autorisé.")
    else:
        if draft_number >= settings.MEMBERS_MAX_REVIEW_DRAFTS:
            raise PermissionError("Ce membre a atteint son nombre de brouillons de reviews maximal autorisé.")


def check_reply_permission(post_type, creation_user):
    """Vérifie la permission de réponse à review de l'utilisateur"""

    if creation_user == post_type.creation_user:
        raise PermissionError("Un utilisateur ne peut pas répondre à sa propre review / r-à-r.")
    elif post_type.replies.filter(creation_user=creation_user):
        raise PermissionError("Cet utilisateur a déjà répondu à cette review / r-à-r.")
    elif hasattr(post_type, "work"):
        if hasattr(post_type.work, "authors"):
            if creation_user not in post_type.work.authors.all():
                raise PermissionError("Seul un auteur peut répondre à une review concernant son œuvre.")
        elif creation_user != post_type.work:
            raise PermissionError("Seul un auteur peut répondre à une review le concernant.")


def check_grading_value(grading):
    if (not isinstance(grading, int)) or (grading < MIN_GRADING_VALUE) or (grading > MAX_GRADING_VALUE):
        raise ValueError(f"La note doit être un nombre entier compris entre {MIN_GRADING_VALUE} et {MAX_GRADING_VALUE}.")


class ReviewManager(models.Manager):
    """Gestionnaire de reviews"""

    def create(self, creation_user, work, text, grading: int = None, draft=False, **extra_fields):

        assert hasattr(work, "reviews")  # vérification que l'objet peut être reviewé

        if grading:
            check_grading_value(grading)

        check_review_permission(reviewed_element=work, creation_user=creation_user)

        if draft:
            check_draft_permission(creation_user=creation_user)

        parsed_text = parse_text(text)

        review = self.model(
            creation_user=creation_user,
            work=work,
            grading=grading,
            draft=draft,
        )

        review.save()

        try:
            review.create_text_version(creation_user=creation_user, text=parsed_text)
        except Exception:
            review.delete()

        return review


class Review(DatedModel, CreatedModel, TextDependentModel):
    """Modèle de review"""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    work = GenericForeignKey('content_type', 'object_id')

    draft = models.BooleanField(verbose_name="brouillon")
    grading = models.PositiveSmallIntegerField(verbose_name="notation", null=True, blank=True,
                                               validators=[MinValueValidator(limit_value=MIN_GRADING_VALUE),
                                                           MaxValueValidator(limit_value=MAX_GRADING_VALUE)])
    objects = ReviewManager()

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

    def create_text_version(self, creation_user, text):
        """Crée une nouvelle version du texte de review par l'utilisateur passé"""

        version = ReviewTextVersion.objects.create(
            review=self,
            text=text,
            creation_user=creation_user or self.creation_user,
            creation_time=timezone.now(),
        )
        version.save()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class ReviewReplyManager(models.Manager):
    """Gestionnaire de réponses à reviews"""

    def create(self, creation_user, text: str, review=None, parent=None, **extra_fields):

        assert not (review and parent)  # La r-à-r ne peut pas répondre à une review et à une r-à-r
        assert (review or parent)  # La r-à-r doit répondre à une review ou à une r-à-r

        check_reply_permission(post_type=review or parent, creation_user=creation_user)

        review_reply = self.model(
            creation_user=creation_user,
            text=text,
            review=review,
            parent=parent
        )

        review_reply.save()

        return review_reply


class ReviewReply(DatedModel, CreatedModel):
    """Modèle de réponse à review"""

    review = models.ForeignKey(verbose_name="review", related_name="replies",
                               to=Review, null=True, on_delete=models.CASCADE,
                               editable=False)
    parent = models.ForeignKey(verbose_name="parent", to="self", null=True,
                               related_name="replies", on_delete=models.CASCADE,
                               editable=False)
    text = models.TextField(verbose_name="texte", blank=False)

    objects = ReviewReplyManager()

    class Meta:
        verbose_name = "réponse à review"
        verbose_name_plural = "réponses à reviews"

    def __str__(self):
        return self.text[:50]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
