from django.db import models
from django.utils import timezone
from core.models import DatedModel, CreatedModel


class OpenCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_closed=False)


class Category(DatedModel, CreatedModel):
    """Modèle de catégorie de caractéristiques"""

    name = models.CharField(verbose_name="nom", max_length=50,
                            blank=False)
    min_limit = models.PositiveSmallIntegerField(verbose_name="minimum")
    max_limit = models.PositiveSmallIntegerField(verbose_name="maximum", null=True, blank=True)
    is_closed = models.BooleanField(verbose_name="restreinte")

    objects = models.Manager()
    open = OpenCategoryManager()

    class Meta:
        verbose_name = "catégorie"
        constraints = [
            models.CheckConstraint(
                name="min_not_over_max",
                check=models.Q(min_limit__lte=models.F("max_limit")),
            )
        ]

    def __str__(self):
        return self.name


class AllowedFeatureManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_forbidden=False)


class Feature(DatedModel, CreatedModel):
    """Modèle de caractéristique"""

    name = models.CharField(verbose_name="nom", max_length=50)
    description = models.TextField(verbose_name="description", null=True, blank=True)
    category = models.ForeignKey(verbose_name="catégorie", to=Category,
                                 related_name="features", on_delete=models.CASCADE,
                                 help_text="Si un parent est indiqué, sa catégorie prévaut.")
    parent = models.ForeignKey(to="self", on_delete=models.CASCADE, null=True, blank=True, default=None,
                               verbose_name="parent", related_name="children",
                               limit_choices_to={"parent": None})  # s'applique aux formulaires seulement
    is_highlighted = models.BooleanField(verbose_name="mise en avant", default=False)
    is_personal = models.BooleanField(verbose_name="personnelle", default=False)
    is_forbidden = models.BooleanField(verbose_name="interdite", default=False)
    replace_with = models.ForeignKey(to="self", on_delete=models.SET_NULL, null=True, blank=True, default=None,
                                     verbose_name="remplacer par", related_name="remplace",
                                     limit_choices_to={"is_forbidden": False})  # idem

    objects = models.Manager()
    allowed = AllowedFeatureManager()

    class Meta:
        verbose_name = "caractéristique"
        order_with_respect_to = "category"
        constraints = [
            models.UniqueConstraint(
                name="unique_name",
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
                fiction.features.add(replace_with)
        self.fiction_set.clear()

        for child in self.children.all():
            child.ban(modification_user=modification_user, replace_with=None)

        self.save()

    # Ceci fonctionne pour empêcher la récursion, mais pas si on appelle parent.children.add(enfant)...
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if hasattr(self.parent, "parent"):
            if self.parent.parent:
                raise RecursionError("La caractéristique parente est déjà sous-ordonnée.")
            self.category = self.parent.category  # Impose que la catégorie de l'enfant soit celle du parent
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)
