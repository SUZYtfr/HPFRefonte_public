from django.db import models
from ordered_model.models import OrderedModel

from core.models import DatedModel, CreatedModel, AuthoredModel, FeaturedModel


class Collection(DatedModel, CreatedModel, AuthoredModel, FeaturedModel):
    """Modèle de série"""

    class Access(models.IntegerChoices):
        CLOSED = (1, "Fermée")
        MODERATED = (2, "Modérée")
        OPEN = (3, "Ouverte")

    title = models.CharField(
        verbose_name="titre",
        max_length=200,
    )
    summary = models.TextField(
        verbose_name="résumé",
    )
    status = models.SmallIntegerField(
        verbose_name="état",
        choices=Access.choices,
        default=Access.CLOSED,
    )
    parent = models.ForeignKey(
        verbose_name="série parente",
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="subcollections",
    )

    fictions = models.ManyToManyField(
        verbose_name="fictions",
        to="fictions.Fiction",
        through="FictionCollectionPosition",
        related_name="collections",
    )

    @property
    def published_reviews(self):
        return self.reviews.filter(draft=False)

    @property
    def mean(self):
        """Renvoie la moyenne des reviews publiées"""

        all_gradings = self.published_reviews.filter(grading__isnull=False).values_list("grading", flat=True)

        if all_gradings:  # pour éviter une division par 0
            return sum(filter(None, all_gradings)) / len(all_gradings)

    @property
    def review_count(self):
        """Renvoie le nombre de reviews publiées"""
        return self.published_reviews.count()

    @property
    def fiction_count(self):
        """Renvoie le compte de fictions"""

        return self.fictions.count()

    class Meta:
        verbose_name = "série"

    def __str__(self):
        return self.title


class FictionCollectionPosition(OrderedModel):

    collection = models.ForeignKey(
        to=Collection,
        on_delete=models.CASCADE,
    )
    fiction = models.ForeignKey(
        to="fictions.Fiction",
        on_delete=models.CASCADE,
    )

    order_with_respect_to = "collection"

    class Meta:
        ordering = ["collection", "order"]
        constraints = [
            models.UniqueConstraint(
                name="UQ_colls_fictioncollectionposition_collection_fiction",
                fields=["collection", "fiction"],
            ),
            models.UniqueConstraint(
                name="UQ_colls_fictioncollectionposition_collection_order",
                fields=["collection", "fiction"],
            )
        ]

    def __repr__(self):
        return self.collection.title[:15] + " <-> " + self.fiction.title[:15]

    def __str__(self):
        return self.__repr__()
