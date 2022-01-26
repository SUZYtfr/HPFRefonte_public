from django.db import models
from ordered_model.models import OrderedModel

from core.models import DatedModel, CreatedModel, AuthoredModel, FeaturedModel, ReviewableModel, FullCleanModel


class CollectionManager(models.Manager):
    """Gestionnaire de séries"""

    def create(self, creation_user, **extra_fields):

        collection = self.model(
            creation_user=creation_user,
            **extra_fields
        )

        collection.save()

        # Sauvegarde > ID Série > Possibilité d'assignation d'autorat
        collection.authors.add(creation_user)

        return collection


class Collection(DatedModel, CreatedModel, AuthoredModel, FeaturedModel, ReviewableModel, FullCleanModel):
    """Modèle de série"""

    class CollectionAccess(models.IntegerChoices):
        CLOSED = (1, "Fermée")
        MODERATED = (2, "Modérée")
        OPEN = (3, "Ouverte")

    title = models.CharField(verbose_name="titre", max_length=200)
    summary = models.TextField(verbose_name="résumé")
    status = models.SmallIntegerField(verbose_name="état",
                                      choices=CollectionAccess.choices,
                                      default=CollectionAccess.CLOSED)

    chapters = models.ManyToManyField(to="fictions.Chapter", verbose_name="chapitres",
                                      through="ChapterCollectionPosition",
                                      related_name="collections")

    objects = CollectionManager()

    class Meta:
        verbose_name = "série"

    def __str__(self):
        return self.title


class ChapterCollectionPosition(OrderedModel):

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    chapter = models.ForeignKey("fictions.Chapter", on_delete=models.CASCADE)

    order_with_respect_to = "collection"

    class Meta:
        ordering = ["collection", "order"]

    def __repr__(self):
        return self.collection.title[:15] + " <-> " + self.chapter.title[:15]

    def __str__(self):
        return self.__repr__()
