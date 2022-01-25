from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Report(models.Model):
    """Modèle de signalement"""

    class Meta:
        verbose_name = "signalement"

    class ReportStatusChoices(models.TextChoices):
        OPEN = ("ouvert", "Ouvert",)
        PENDING = ("traité", "En cours de traitement",)
        CLOSE = ("clôt", "Clôt",)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, editable=False)
    object_id = models.PositiveIntegerField(editable=False)
    object = GenericForeignKey('content_type', 'object_id')
    element = models.CharField(max_length=255, verbose_name="élément", null=True, blank=True)  # pour préciser quel élément de l'objet particulièrement (titre, note, bio... ?)

    report_user = models.ForeignKey(verbose_name="signaleur", to="users.User", on_delete=models.CASCADE, related_name="+", editable=False)
    datetime = models.DateTimeField(verbose_name="horodatage", editable=False)
    argument = models.TextField(verbose_name="justification")

    status = models.CharField(max_length=10, verbose_name="statut", choices=ReportStatusChoices.choices, default=ReportStatusChoices.OPEN)
    comment = models.TextField(verbose_name="commentaire", blank=True)

