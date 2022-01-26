from django.db import models
from django.conf import settings
from core.models import get_user_deleted_sentinel, FullCleanModel
from core.text_functions import count_words

class BaseTextVersionModel(FullCleanModel):
    """Modèle de base pour les versions de textes"""

    class Meta:
        abstract = True

    text = models.TextField(verbose_name="texte")
    creation_time = models.DateTimeField(verbose_name="création", editable=False)
    creation_user = models.ForeignKey(verbose_name="créateur", editable=False, related_name="+",
                                      to=settings.AUTH_USER_MODEL, on_delete=models.SET(get_user_deleted_sentinel))

    def __str__(self):
        return "{:25} ({})".format(str(self.text), self.creation_time.strftime("%d/%m/%y, %H:%M"))


class ChapterTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de chapitre"""

    class Meta:
        verbose_name = "version de texte de chapitre"

    chapter = models.ForeignKey(verbose_name="chapitre", editable=False, related_name="versions",
                                to="fictions.Chapter", on_delete=models.CASCADE)
    word_count = models.IntegerField(editable=False, verbose_name="compte de mots")

    # def __str__(self):
    #     return "{:25} ({})".format(str(self.chapter), self.creation_time.strftime("%d/%m/%y, %H:%M"))


class ReviewTextVersion(BaseTextVersionModel):
    """Modèle de version de texte de review"""

    class Meta:
        verbose_name = "version de texte de review"

    review = models.ForeignKey(verbose_name="review", editable=False, related_name="versions",
                               to="reviews.Review", on_delete=models.CASCADE)

    # def __str__(self):
    #     return "{:25} ({})".format(str(self.review), self.creation_time.strftime("%d/%m/%y, %H:%M"))
