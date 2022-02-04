from django.db import models
from django.utils import timezone

from core.models import CreatedModel, DatedModel

from users.models import User


class PollGroup(DatedModel, CreatedModel):
    """Modèle de groupe de sondage"""

    class Meta:
        verbose_name = "groupe de sondage"
        verbose_name_plural = "groupes de sondages"

    title = models.CharField(verbose_name="titre", max_length=50)

    def __str__(self):
        return self.title


class PollQuestionManager(models.Manager):
    """Gestionnaire de questions de sondage"""

    def create(self, **kwargs):

        chapter = kwargs.pop("chapter", None)
        selection = kwargs.pop("selection", None)

        assert not all([chapter, selection])

        poll_question = self.model(
            **kwargs,
        )
        poll_question.save()

        if chapter:
            chapter.poll = poll_question
            chapter.save()
        if selection:
            selection.poll = poll_question
            selection.save()

        return poll_question


class PollQuestion(DatedModel, CreatedModel):
    """Modèle de question de sondage"""

    poll_group = models.ForeignKey(verbose_name="groupe", to=PollGroup,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name="questions")
    question_text = models.CharField(verbose_name="texte", max_length=500)
    max_choices = models.PositiveSmallIntegerField(verbose_name="nombre de choix autorisé",
                                                   default=1,
                                                   help_text="Pour les sondages de sélection, ce paramètre est ignoré.")
    opening_datetime = models.DateTimeField(verbose_name="ouverture", default=timezone.now)
    closing_datetime = models.DateTimeField(verbose_name="clôture", null=True, blank=True, default=None)
    members_only = models.BooleanField(verbose_name="réservé", default=True)
    visibility = models.BooleanField(verbose_name="visibilité", default=True)

    objects = PollQuestionManager()

    class Meta:
        verbose_name = "question de sondage"
        verbose_name_plural = "questions de sondage"
        order_with_respect_to = "poll_group"

    def __str__(self):
        return self.question_text

    def get_top_choices(self, number_of_top_choices=1, flat_count=True):
        """Renvoie les premiers choix de la question

            Si flat_count=True, le résultat est produit selon le décompte des voix de chaque réponse.
            Si flat_count=False, le résultat est produit selon la somme des points des voix de chaque réponse.
        """

        if flat_count:
            return self.answers.annotate(total_votes=models.Count("votes")).order_by("-total_votes")[:number_of_top_choices]
        else:
            return self.answers.annotate(total_points=models.Sum("votes__points")).order_by("-total_points")[:number_of_top_choices]

    @property
    def is_open(self):
        return self.closing_datetime or timezone.now() < timezone.now()

    def close_poll(self, **kwargs):
        """Ferme le sondage"""

        if self.is_open:
            self.closing_datetime = timezone.now()
            modification_user = kwargs.pop("modification_user", None)
            if modification_user:
                self.modification_user = modification_user
                self.modification_date = timezone.now()
            self.save()
        return self.is_open


class PollAnswer(DatedModel, CreatedModel):
    """Modèle de réponse de sondage"""

    poll_question = models.ForeignKey(verbose_name="question", to=PollQuestion,
                                      on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(verbose_name="texte", max_length=500)

    class Meta:
        verbose_name = "réponse de sondage"
        verbose_name_plural = "réponses de sondages"
        order_with_respect_to = "poll_question"

    def __str__(self):
        return self.answer_text

    @property
    def points(self):
        return sum(self.votes.values_list("points", flat=True))


class BallotManager(models.Manager):
    """Gestionnaire de bulletins"""

    def cast(self, user, ip_address, vote_datetime, poll_question, answers):
        """Crée le ballot et les votes"""

        ballot = self.model(
            user=user if not user.is_anonymous else None,
            ip_address=ip_address,
            poll_question=poll_question,
            vote_datetime=vote_datetime,
        )
        ballot.save()

        try:
            pollvotes = [PollVote(poll_answer=answer, ballot=ballot, points=points) for points, answer in answers]
            PollVote.objects.bulk_create(pollvotes)
        except Exception:
            ballot.delete()  # On ne veut pas un bulletin vide si quelconque problème survient
            raise

        return ballot

    # def bulk_create(self, user, ip_address, vote_datetime, poll_question, choices: list):
    #     """Effectue le vote pour un groupe de sondage"""
    #
    #     try:
    #         verify_choices(poll_question, choices)
    #         if len(choices) != poll_question.answers.count():
    #             raise ValidationError("Tous les ID de réponses doivent être classés.")
    #         answers = enumerate(reversed([PollAnswer.objects.get(pk=x) for x in choices]), start=1)
    #     except ValidationError:
    #         raise
    #
    #     return self.cast(user, ip_address, vote_datetime, poll_question, answers)

    def create(self, user, ip_address, vote_datetime, poll_question, choices: list):
        """Effectue le vote pour une question de sondage"""

        if hasattr(poll_question, "selection"):
            answers = enumerate(reversed(choices), start=1)
        else:
            answers = [(1, choice) for choice in choices]

        return self.cast(user, ip_address, vote_datetime, poll_question, answers)


class Ballot(models.Model):
    """Modèle de bulletin"""

    user = models.ForeignKey(verbose_name="votant", to=User, on_delete=models.SET_NULL, related_name="+",
                             null=True, editable=False)
    ip_address = models.GenericIPAddressField(verbose_name="adresse IP", editable=False)
    vote_datetime = models.DateTimeField(verbose_name="horodatage du vote", default=timezone.now, editable=False)
    poll_question = models.ForeignKey(to=PollQuestion, on_delete=models.CASCADE)

    objects = BallotManager()

    class Meta:
        verbose_name = "bulletin"
        constraints = [
            models.UniqueConstraint(
                name="unique_user_per_poll_question",
                fields=["user", "poll_question"],
            ),
            models.UniqueConstraint(
                name="unique_ip_per_poll_question",
                fields=["ip_address", "poll_question"],
            ),
        ]

    def __str__(self):
        return f"Bulletin {('de ' + str(self.user)) if self.user else 'anonyme'} pour {self.poll_question}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class PollVote(models.Model):
    """Modèle de vote"""

    ballot = models.ForeignKey(to=Ballot, on_delete=models.CASCADE)
    poll_answer = models.ForeignKey(verbose_name="réponse", to=PollAnswer, on_delete=models.CASCADE,
                                    related_name="votes")
    points = models.PositiveSmallIntegerField(verbose_name="points", default=1)

    class Meta:
        verbose_name = "vote"
        constraints = [
            models.UniqueConstraint(
                name="unique_answer_per_ballot",
                fields=["ballot", "poll_answer"]
            )
        ]

    def __str__(self):
        return f"1 vote pour {self.poll_answer}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
