from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.conf import settings


class FullCleanModel(models.Model):
    """Implémente la validation lors de l'enregistrement du modèle"""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        super().save(force_insert=False, force_update=False, using=None,
                     update_fields=None)

    class Meta:
        abstract = True


class DatedModel(FullCleanModel):
    """Modèle de base implémentant la date de création et modification"""

    creation_date = models.DateTimeField(verbose_name="création",
                                         default=timezone.now,
                                         editable=False)
    modification_date = models.DateTimeField(verbose_name="modification",
                                             null=True, blank=True,
                                             editable=False)

    class Meta:
        abstract = True


def get_moderation_account():
    """Renvoie le compte de modération"""
    return get_user_model().objects.get(pk=settings.MODERATION_ACCOUNT_ID)


# En cas de suppression pure et dure d'un compte créateur ou modificateur d'un élément, remplacement par la sentinelle
# Permet de conserver par exemple une fiction dont le créateur supprimant son compte n'était plus l'auteur
# Cette sentinelle concerne la BBD, les règles d'autorat sont déterminées au niveau des modèles
def get_user_deleted_sentinel():
    """Renvoie le compte sentinelle"""
    return get_user_model().objects.get(pk=settings.SENTINEL_ACCOUNT_ID)


class CreatedModel(FullCleanModel):
    """Modèle de base implémentant le créateur et modificateur"""

    creation_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      verbose_name="créateur",
                                      related_name="created_%(class)ss",
                                      on_delete=models.SET(get_user_deleted_sentinel),
                                      editable=False)
    modification_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                          verbose_name="modificateur",
                                          related_name="modified_%(class)ss",
                                          on_delete=models.SET(get_user_deleted_sentinel),
                                          null=True, blank=True,
                                          editable=False)

    class Meta:
        abstract = True


class AuthoredModel(FullCleanModel):
    """Modèle de base implémentant l'autorat"""

    # https://docs.djangoproject.com/fr/3.1/topics/db/models/#be-careful-with-related-name-and-related-query-name
    authors = models.ManyToManyField(to=settings.AUTH_USER_MODEL,
                                     verbose_name="auteurs",
                                     related_name="authored_%(class)ss")

    class Meta:
        abstract = True


class FeaturedModel(FullCleanModel):
    """Modèle de base implémentant l'assignation de caractéristiques"""

    class Meta:
        abstract = True

    features = models.ManyToManyField(verbose_name="caractéristiques",
                                      to="features.Feature")


class ReviewableModel(FullCleanModel):
    """Modèle de base implémentant les reviews"""

    class Meta:
        abstract = True

    reviews = GenericRelation("reviews.Review", related_query_name="%(class)s")

    @property
    def mean(self):
        """Renvoie la moyenne de toutes les reviews notées et publiées de cet objet"""

        all_gradings = self.reviews.filter(draft=False, grading__isnull=False).values_list("grading", flat=True)

        if all_gradings:  # pour éviter division par 0
            return sum(filter(None, all_gradings)) / len(all_gradings)
        return None


class TextDependentModel(FullCleanModel):
    """Modèle de base implémentant le traitement de texte"""

    class Meta:
        abstract = True

    def create_text_version(self, creation_user, text):
        """Réécrit par les classes héritées"""
        pass

    @property
    def text(self):
        """Renvoie la dernière version en date du texte"""
        if version := self.versions.last():
            return version.text

    @text.setter
    def text(self, text):
        """Enregistre une version du texte si celui-ci a changé"""
        if text != self.text:
            self.create_text_version(creation_user=self.creation_user, text=text)

    # TODO - Implémenter ces méthodes
    def get_text_version(self, date=None, step=None):
        """Renvoie la version du texte la plus proche ultérieure à une date ou une étape"""
        pass

    def compare_text_versions(self, date=None, step=None):
        """Renvoie la comparaison du texte actuel avec la version la plus proche ultérieure à une date, etc"""
        pass
