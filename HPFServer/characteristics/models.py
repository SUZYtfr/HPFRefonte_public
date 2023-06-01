from django.db import models
from django.utils import timezone
from core.models import DatedModel, CreatedModel
from fictions.models import Chapter
from fictions.enums import ChapterValidationStage


class CharacteristicTypeQuerySet(models.QuerySet):
    def open(self):
        return self.filter(is_closed=False)


class CharacteristicType(DatedModel, CreatedModel):
    """Modèle de type de caractéristiques"""

    name = models.CharField(
        verbose_name="nom",
        max_length=50,
        blank=False,
    )
    min_limit = models.PositiveSmallIntegerField(
        verbose_name="minimum",
    )
    max_limit = models.PositiveSmallIntegerField(
        verbose_name="maximum",
        null=True,
        blank=True,
    )
    is_closed = models.BooleanField(
        verbose_name="restreinte",
    )

    objects = CharacteristicTypeQuerySet.as_manager()

    class Meta:
        verbose_name = "type de caractéristiques"
        verbose_name_plural = "types de caractéristiques"
        constraints = [
            models.CheckConstraint(
                name="CK_characteristics_characteristictype_min_limit_lte_max_limit",
                check=models.Q(min_limit__lte=models.F("max_limit")),
            )
        ]

    def __str__(self):
        return self.name


class CharacteristicQuerySet(models.QuerySet):
    def allowed(self):
        return self.filter(is_forbidden=False)

    def forbidden(self):
        return self.filter(is_forbidden=True)

    def fiction_counts(self):
        fiction_count = models.Count(
            "fiction",
            models.Q(fiction__chapters__validation_status=ChapterValidationStage.PUBLISHED)
        )
        return self.annotate(fiction_count=fiction_count)


class Characteristic(DatedModel, CreatedModel):
    """Modèle de caractéristique"""

    name = models.CharField(
        verbose_name="nom",
        max_length=50,
    )
    description = models.TextField(
        verbose_name="description",
        null=True,
        blank=True,
    )
    characteristic_type = models.ForeignKey(
        verbose_name="type de caractéristiques",
        to=CharacteristicType,
        related_name="characteristics",
        on_delete=models.CASCADE,
        help_text="Si un parent est indiqué, son type de caractéristiques prévaut.",
    )
    parent = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        verbose_name="parent",
        related_name="children",
        limit_choices_to={"parent": None},
    )  # s'applique aux formulaires seulement
    is_highlighted = models.BooleanField(
        verbose_name="mise en avant",
        default=False,
    )
    is_personal = models.BooleanField(
        verbose_name="personnelle",
        default=False,
    )
    is_forbidden = models.BooleanField(
        verbose_name="interdite",
        default=False,
    )
    replace_with = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name="remplacer par",
        related_name="remplace",
        limit_choices_to={"is_forbidden": False},
    )  # idem

    objects = CharacteristicQuerySet.as_manager()

    class Meta:
        verbose_name = "caractéristique"
        order_with_respect_to = "characteristic_type"
        constraints = [
            models.UniqueConstraint(
                name="UQ_characteristics_characteristic_name",
                fields=["name"],
            )
        ]

    def __str__(self):
        return self.name

    def ban(self, modification_user, replace_with=None):
        """Interdit l'usage de la caractéristique
        - Indique que la caractéristique est interdite
        - Indique la règle de remplacement
        - Retire le parent de la caractéristique
        - Le cas échéant, retire la caractéristique de toutes les fictions, ou la remplace par celle qui est indiquée
        - Appelle cette fonction pour chaque enfant de la caractéristique (sans règle de remplacement)
        """

        self.is_forbidden = True
        self.replace_with = replace_with
        self.parent = None
        self.modification_user = modification_user
        self.modification_date = timezone.now()
        if replace_with:
            for fiction in self.fiction_set.all():
                fiction.characteristics.add(replace_with)
        self.fiction_set.clear()

        for child in self.children.all():
            child.ban(modification_user=modification_user, replace_with=None)

        self.save()

    # Ceci fonctionne pour empêcher la récursion, mais pas si on appelle parent.children.add(enfant)...
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if hasattr(self.parent, "parent"):
            if self.parent.parent:
                raise RecursionError("La caractéristique parente est déjà sous-ordonnée.")
            self.characteristic_type = self.parent.characteristic_type  # Impose que la catégorie de l'enfant soit celle du parent
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
