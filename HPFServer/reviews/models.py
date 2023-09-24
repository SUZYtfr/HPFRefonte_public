from django.db import models, transaction
from django.utils import timezone
from django.core import validators
from mptt import models as mptt_models

from core.models import (
    DatedModel,
    CreatedModel,
    TextDependentModel,
    BaseTextVersionModel,
)
from fictions.models import (
    Fiction,
    Chapter,
    Collection,
)

MIN_GRADING_VALUE = 1
MAX_GRADING_VALUE = 10


'''
def check_draft_permission(creation_user):
    """Vérifie la permission de brouillon de l'utilisateur"""

    draft_number = creation_user.created_reviews.filter(is_draft=True).count()
    if creation_user.has_perm("extra_review_drafts"):
        if draft_number >= settings.PREMIUM_MAX_REVIEW_DRAFTS:
            raise PermissionError("Cet adhérent a atteint son nombre de brouillons de reviews maximal autorisé.")
    else:
        if draft_number >= settings.MEMBERS_MAX_REVIEW_DRAFTS:
            raise PermissionError("Ce membre a atteint son nombre de brouillons de reviews maximal autorisé.")
'''


class ReviewManager(mptt_models.TreeManager):
    @transaction.atomic
    def create(self, creation_user, text, **extra_fields):
        # if self.filter(creation_user=creation_user).exists():
        #     raise utils.IntegrityError
        instance = self.model(
            creation_user=creation_user,
            **extra_fields
        )
        instance.save()
        instance.versions.create(
            creation_user=creation_user,
            text=text,
        )
        return instance
    
    '''
    def create_anonymous(self, email, **extra_fields):
        creation_user = User.objects.filter(email=email).first()
        if creation_user:
            if creation_user.is_active:
                raise
        else:
            creation_user = User.objects.create_anonymous_user(email, **extra_fields)
        return self.create(creation_user=creation_user, **extra_fields)
    '''
        
    def published(self):
        return self.filter(is_draft=False)


class Review(mptt_models.MPTTModel, DatedModel, CreatedModel):
    """
    Modèle abstrait de review et réponse à review
    
    Ce modèle abstrait ordonne les reviews et réponses à reviews les unes aux autres
    en arborescence à l'aide de la technique MPTT :
    https://django-mptt.readthedocs.io/en/latest/index.html
    Ce modèle abstrait comporte les champs communs à tous les types de reviews.
    Il est concrétisé par les types particuliers de reviews qui ajoutent le lien
    vers la ressource en question (fiction, chapitre, série).
    Chaque type de review (et réponse à review) a donc sa propre table ainsi que sa
    propre table de versions de texte associée, ce qui permet de pouvoir le
    différencier des autres dans le futur, par exemple en rajoutant un champ
    spécifique à ce type de review.
    Les modèles concrets introduisent deux contraintes :
    - Une review (de premier niveau) peut contenir une note mais pas un lien vers
      une review parente ; réciproquement, une réponse à review doit comporter un 
      lien vers un parent, mais pas une note.
      Contrainte : (NOT (level>0 AND grading NOT NULL))
    - Une réponse à review (de niveau supérieur) ne peut contenir un lien vers une 
      ressource (fiction, chapitre, série), et vers un parent.
      Cela permet de récupérer facilement les reviews de premier niveau depuis la 
      ressource en question (ex. fiction.reviews.all()) plutôt que de devoir les
      filtrer, et accentue la distinction entre review et réponse à review pour 
      éviter la confusion par exemple d'une review et de sa réponse ne portant 
      accidentellement pas sur la même ressource).
      Contrainte : (level>0 XOR fiction NULL)
    """

    class Meta:
        abstract = True

    parent = mptt_models.TreeForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_draft = models.BooleanField(
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

    @property
    def reply_count(self) -> int:
        return self.get_descendant_count()

    @property
    def with_scale(self) -> str:
        """Renvoie la notation suivie de la mesure de notation"""

        return f"{str(self.grading or '-')}/10"

    def create_text_version(self, text: str, creation_user_id: int = None, touch: bool = True):
        """Crée une nouvelle version du texte de review par l'utilisateur passé"""
    
        version = self.versions.create(
            text=text,
            creation_user_id=creation_user_id or self.creation_user_id,
            creation_date=timezone.now(),
        )
        version.save()
    
        if touch:  # à utiliser en cas de modification
            self.save()

    @property
    def text(self) -> str:
        latest_version = self.versions.latest("creation_date")
        return getattr(latest_version, "text", "")

    def __str__(self) -> str:
        subtype = "review" if self.get_level() <= 0 else "réponse"
        return f"« {self.text[:50]} » ({subtype})"


class FictionReview(Review, TextDependentModel):
    class Meta:
        abstract = False
        verbose_name = "review de fiction"
        verbose_name_plural = "reviews de fictions"
        constraints = [
            models.CheckConstraint(
                name="CK_%(app_label)s_%(class)s_not_leaf_and_grading",
                check=~models.Q(level__gt=0, grading__isnull=False),
            ),
            models.CheckConstraint(
                name="CK_%(app_label)s_%(class)s_leaf_xor_fiction_null",
                check=models.Q(level__gt=0) ^ models.Q(fiction__isnull=False),
            ),
        ]
    
    objects = ReviewManager()

    fiction = models.ForeignKey(
        to=Fiction,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="reviews",
        editable=True,
    )


class ChapterReview(Review, TextDependentModel):
    class Meta:
        verbose_name = "review de chapitre"
        verbose_name_plural = "reviews de chapitres"
        constraints = [
            models.CheckConstraint(
                name="CK_%(app_label)s_%(class)s_not_leaf_and_grading",
                check=~models.Q(level__gt=0, grading__isnull=False),
            ),
            models.CheckConstraint(
                name="CK_%(app_label)s_%(class)s_leaf_xor_chapter_null",
                check=models.Q(level__gt=0) ^ models.Q(chapter__isnull=False),
            ),
        ]

    objects = ReviewManager()

    chapter = models.ForeignKey(
        to=Chapter,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="chapitre",
        related_name="reviews",
        editable=True,
    )


class CollectionReview(Review, TextDependentModel):
    class Meta:
        verbose_name = "review de série"
        verbose_name_plural = "reviews de séries"
        constraints = [
            models.CheckConstraint(
                name="CK_%(app_label)s_%(class)s_not_leaf_and_grading",
                check=~models.Q(level__gt=0, grading__isnull=False),
            ),
            models.CheckConstraint(
                name="CK_%(app_label)s_%(class)s_leaf_xor_collection_null",
                check=models.Q(level__gt=0) ^ models.Q(collection__isnull=False),
            ),
        ]
    
    objects = ReviewManager()

    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="série",
        related_name="reviews",
        editable=True,
    )


class FictionReviewTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de review de fiction"""

    class Meta:
        verbose_name = "version de texte de review de fiction"
        verbose_name_plural = "versions de textes de reviews de fictions"

    review = models.ForeignKey(
        editable=True,
        related_name="versions",
        to="reviews.FictionReview",
        on_delete=models.CASCADE,
    )


class ChapterReviewTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de review de chapitre"""

    class Meta:
        verbose_name = "version de texte de review de chapitre"
        verbose_name_plural = "versions de textes de reviews de chapitres"

    review = models.ForeignKey(
        editable=True,
        related_name="versions",
        to="reviews.ChapterReview",
        on_delete=models.CASCADE,
    )


class CollectionReviewTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de review de série"""

    class Meta:
        verbose_name = "version de texte de review de série"
        verbose_name_plural = "versions de textes de reviews de séries"

    review = models.ForeignKey(
        editable=True,
        related_name="versions",
        to="reviews.CollectionReview",
        on_delete=models.CASCADE,
    )
