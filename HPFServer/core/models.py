from django.db import models
from django.conf import settings
from core.utils import get_user_deleted_sentinel


class DatedModel(models.Model):
    """Modèle de base implémentant la date de création et modification"""

    creation_date = models.DateTimeField(
        verbose_name="création",
        auto_now_add=True,
    )
    modification_date = models.DateTimeField(
        verbose_name="modification",
        null=True,
        auto_now=True,
    )

    class Meta:
        abstract = True


class CreatedModel(models.Model):
    """Modèle de base implémentant le créateur et modificateur"""

    creation_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="créateur",
        related_name="created_%(class)ss",
        on_delete=models.SET(get_user_deleted_sentinel),
        editable=True,
    )
    modification_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="modificateur",
        # related_name="modified_%(class)ss",
        related_name="+",
        on_delete=models.SET(get_user_deleted_sentinel),
        null=True,
        blank=True,
        editable=True,
    )

    class Meta:
        abstract = True


class AuthoredModel(models.Model):
    """Modèle de base implémentant l'autorat"""

    # https://docs.djangoproject.com/fr/3.1/topics/db/models/#be-careful-with-related-name-and-related-query-name
    authors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        verbose_name="auteur·ices",
        related_name="authored_%(class)ss",
    )

    class Meta:
        abstract = True


class CharacteristicModel(models.Model):
    """Modèle de base implémentant l'assignation de caractéristiques"""

    class Meta:
        abstract = True

    characteristics = models.ManyToManyField(
        to="characteristics.Characteristic",
        verbose_name="caractéristiques",
    )


class TextDependentModel(models.Model):
    """Modèle de base implémentant le traitement de texte"""

    class Meta:
        abstract = True

    @property
    def text(self):
        """Renvoie la dernière version en date du texte"""

        return getattr(self.versions.latest("creation_date"), "text", "")

    @property
    def word_count(self) -> int | None:
        return getattr(self, "_word_count", None) or getattr(self.versions.last(), "word_count", None)
    word_count.fget.short_description = "compte de mots"

    # TODO - Implémenter ces méthodes
    def get_text_version(self, date=None, step=None):
        """Renvoie la version du texte la plus proche ultérieure à une date ou une étape"""
        pass

    def compare_text_versions(self, date=None, step=None):
        """Renvoie la comparaison du texte actuel avec la version la plus proche ultérieure à une date, etc"""
        pass


class BaseTextVersionModel(models.Model):
    """Modèle de base pour les versions de textes"""

    class Meta:
        abstract = True

    text = models.TextField(
        verbose_name="texte",
        editable=True,
    )
    creation_date = models.DateTimeField(
        verbose_name="création",
        auto_now_add=True,
        editable=True,
    )
    creation_user = models.ForeignKey(
        verbose_name="créateur",
        editable=True,
        related_name="+",
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_user_deleted_sentinel),
    )

    def __str__(self):
        return "{0} ({1})".format(str(self.text)[:50], self.creation_date.strftime("%d/%m/%y, %H:%M"))
