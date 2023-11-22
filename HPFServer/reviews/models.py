from django.db import IntegrityError
from django.db.transaction import atomic
from django.db.models import (
    BooleanField,
    PositiveSmallIntegerField,
    DateTimeField,
    ForeignKey,
    CASCADE,
    F,
)
from django.core.validators import MinValueValidator, MaxValueValidator
from polymorphic_tree.models import (
    PolymorphicMPTTModel,
    PolymorphicTreeForeignKey,
)
from polymorphic_tree.managers import PolymorphicMPTTQuerySet
 
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


class ReviewQuerySet(PolymorphicMPTTQuerySet):
    @atomic
    def create(self, creation_user, text, parent=None, **extra_fields):
        if not parent and not self.model.can_be_root: 
            raise IntegrityError("Une réponse à review doit avoir un parent.")
        if parent and self.model.can_be_root:
            raise IntegrityError("Une review ne peut pas avoir de parent.")

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

    def non_archived(self):
        return self.filter(is_archived=False)

    def reviews(self):
        return self.filter(level=0)

    def leaves(self):
        return self.alias(
            boundaries_range=F("rght") - F("lft"),
        ).filter(
            boundaries_range=1,
        )


class BaseReview(DatedModel, CreatedModel, TextDependentModel, PolymorphicMPTTModel):
    """
    Modèle de base de review et réponse à review.
    Si cette base est étendue, c'est une review (porte la notation et le lien vers la ressource)
    Sinon, c'est une réponse à review

    TODO - Les paramètres de classe ne sont pas garantis par la BDD. Pas très probants. Enquêter.
    """

    class Meta:
        verbose_name = "réponse à review"
        verbose_name_plural = "réponses à reviews"

    objects = ReviewQuerySet().as_manager()

    # Paramètres pour les réponses à reviews (à redéclarer dans les sous-classes !)
    can_be_root = False
    can_have_children = True
    child_types = ["self"]

    parent = PolymorphicTreeForeignKey(
        to="self",
        null=True,
        blank=True,
        on_delete=CASCADE,
    )
    is_draft = BooleanField(
        verbose_name="brouillon",
        default=True,
    )
    is_archived = BooleanField(
        verbose_name="archivé",
        default=False,
        help_text="Indique que le destinataire de ce message l'a explicitement marqué comme archivé."
    )
    publication_date = DateTimeField(
        verbose_name="publication",
        null=True,
        blank=True,
    )

    # TODO - réparer ça
    def __str__(self) -> str:
        subtype = "ReviewReply" if self.get_real_instance_class() == self.__class__.__name__ else self.__class__.__name__
        return f"« {self.text[:50]} » ({subtype})"

    @property
    def reply_count(self) -> int:
        return self.get_descendant_count()

    @property
    def with_scale(self) -> str:
        """Renvoie la notation suivie de la mesure de notation"""

        return f"{str(self.grading or '-')}/10"


class CollectionReview(BaseReview):
    class Meta:
        verbose_name = "review de série"
        verbose_name_plural = "reviews de séries"

    # Paramètres pour les reviews
    can_be_root = True
    can_have_children = True
    child_types = [BaseReview]

    collection = ForeignKey(
        to=Collection,
        on_delete=CASCADE,
        related_name="reviews",
    )
    grading = PositiveSmallIntegerField(
        verbose_name="notation",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(limit_value=MIN_GRADING_VALUE),
            MaxValueValidator(limit_value=MAX_GRADING_VALUE),
        ]
    )


class FictionReview(BaseReview):
    class Meta:
        verbose_name = "review de fiction"
        verbose_name_plural = "reviews de fictions"

    # Paramètres pour les reviews
    can_be_root = True
    can_have_children = True
    child_types = [BaseReview]

    fiction = ForeignKey(
        to=Fiction,
        on_delete=CASCADE,
        related_name="reviews",
    )
    grading = PositiveSmallIntegerField(
        verbose_name="notation",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(limit_value=MIN_GRADING_VALUE),
            MaxValueValidator(limit_value=MAX_GRADING_VALUE),
        ]
    )


class ChapterReview(BaseReview):
    class Meta:
        verbose_name = "review de chapitre"
        verbose_name_plural = "reviews de chapitres"

    # Paramètres pour les reviews
    can_be_root = True
    can_have_children = True
    child_types = [BaseReview]

    chapter = ForeignKey(
        to=Chapter,
        on_delete=CASCADE,
        related_name="reviews",
    )
    grading = PositiveSmallIntegerField(
        verbose_name="notation",
        null=True,
        blank=True,
        validators=[
            MinValueValidator(limit_value=MIN_GRADING_VALUE),
            MaxValueValidator(limit_value=MAX_GRADING_VALUE),
        ]
    )


class BaseReviewTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de review et réponse à review"""

    class Meta:
        verbose_name = "version de texte de base de review"
        verbose_name_plural = "versions de textes de bases de reviews"

    base_review = ForeignKey(
        editable=True,
        related_name="versions",
        to="reviews.BaseReview",
        on_delete=CASCADE,
    )


# TODO - ancien modèle non polymorphique, à virer
'''
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
'''