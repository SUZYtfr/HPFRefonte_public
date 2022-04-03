from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group

from core.models import DatedModel, CreatedModel, AuthoredModel


class NewsArticle(DatedModel, CreatedModel, AuthoredModel):
    """Modèle d'actualité"""

    class NewsStatus(models.IntegerChoices):
        PENDING = (1, "En attente")
        DRAFT = (2, "À publier")
        PUBLISHED = (3, "Publiée")

    class NewsCategory(models.IntegerChoices):
        UNDEFINED = (0, "Actualité")
        ASSEMBLY = (1, "Assemblée générale")
        ASSOCIATION = (2, "Association")
        CONTEST = (3, "Concours")
        NIGHTS = (4, "Nuits")
        PODIUM = (5, "Podium")
        PROJECTS = (6, "Projet")

    post_date = models.DateTimeField(verbose_name="parution", default=None, null=True, blank=True)
    title = models.CharField(verbose_name="titre", max_length=255)
    content = models.TextField(verbose_name="contenu")
    category = models.SmallIntegerField(verbose_name="catégorie", choices=NewsCategory.choices)
    status = models.SmallIntegerField(verbose_name="état", choices=NewsStatus.choices,
                                      default=NewsStatus.PENDING)

    teams = models.ManyToManyField(to=Group, related_name="authored_newsarticles")

    class Meta:
        verbose_name = "actualité"

    def __str__(self):
        return self.title

    def post(self, modification_user):
        self.status = self.NewsStatus.PUBLISHED
        self.post_date = timezone.now()
        self.modification_user = modification_user
        self.save()


class NewsComment(DatedModel, CreatedModel):
    """Modèle de commentaire d'actualité"""

    text = models.TextField(verbose_name="texte")
    newsarticle = models.ForeignKey(to=NewsArticle, verbose_name="actualité", related_name="comments",
                                    on_delete=models.CASCADE,
                                    limit_choices_to={"status": NewsArticle.NewsStatus.PUBLISHED},)

    class Meta:
        verbose_name = "commentaire"

    def __str__(self):
        return self.text[:50]
