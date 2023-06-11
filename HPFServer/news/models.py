from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from core.models import DatedModel, CreatedModel, AuthoredModel
from .enums import NewsCategory, NewsStatus


class NewsArticle(DatedModel, CreatedModel, AuthoredModel):
    """Modèle d'actualité"""

    title = models.CharField(
        verbose_name="titre",
        max_length=255,
    )
    post_date = models.DateTimeField(
        verbose_name="horodatage de parution",
        default=None,
        null=True,
        blank=True,
    )
    content = models.TextField(
        verbose_name="contenu",
    )
    category = models.SmallIntegerField(
        verbose_name="catégorie",
        choices=NewsCategory.choices,
    )
    status = models.SmallIntegerField(
        verbose_name="état",
        choices=NewsStatus.choices,
        default=NewsStatus.PENDING,
    )

    teams = models.ManyToManyField(
        to=Group,
        related_name="authored_newsarticles",
    )

    class Meta:
        verbose_name = "actualité"

    def __str__(self):
        return self.title

    @property
    def comment_count(self) -> int:
        return self.comments.count()

    def post(self, modification_user):
        self.status = NewsStatus.PUBLISHED
        self.post_date = timezone.now()
        self.modification_user = modification_user
        self.save()


class NewsComment(DatedModel, CreatedModel):
    """Modèle de commentaire d'actualité"""

    text = models.TextField(
        verbose_name="texte",
    )
    newsarticle = models.ForeignKey(
        to=NewsArticle,
        verbose_name="actualité",
        related_name="comments",
        on_delete=models.CASCADE,
        limit_choices_to={"status": NewsStatus.PUBLISHED},
    )

    class Meta:
        verbose_name = "commentaire"

    def __str__(self):
        return self.text[:50]
