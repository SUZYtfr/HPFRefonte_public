from django.db import models

from core.models import DatedModel, CreatedModel, FullCleanModel

from polls.models import PollGroup, PollQuestion, PollAnswer
from fictions.models import Fiction


class Selection(DatedModel, CreatedModel):
    """Modèle de sélection"""

    theme = models.CharField(verbose_name="thème", max_length=50)
    description = models.TextField(verbose_name="description")
    # vignette
    fictions = models.ManyToManyField(verbose_name="fictions gagnantes",
                                      to="fictions.Fiction",
                                      related_name="selections",
                                      blank=True)
    open = models.BooleanField(verbose_name="ouverte",
                               default=False)
    poll = models.OneToOneField(verbose_name="sondage",
                                to="polls.PollQuestion",
                                on_delete=models.SET_NULL,
                                null=True, blank=True)

    class Meta:
        verbose_name = "sélection"
        constraints = [
            models.UniqueConstraint(
                name="unique_open_selection",
                fields=["open"],
                condition=models.Q(open=True),
            )
        ]

    def __str__(self):
        return self.theme

    def close_and_create_poll(self, creation_user, **kwargs):
        """Clôt la sélection et crée un sondage avec les propositions acceptées"""

        poll = PollGroup.objects.create(
            element=self,
            creation_user=creation_user,
            title=kwargs.get("title", f"Sondage de sélection sur le thème : {self.theme}"),
            opening_datetime=kwargs.get("opening_datetime", None),
            closing_datetime=kwargs.get("closing_datetime", None),
        )

        poll_question = PollQuestion.objects.create(
            poll=poll,
            creation_user=creation_user,
            question_text="Classez les propositions par ordre croissant de préférence.",
            max_choices=len(self.propositions.filter(decision=True)),
        )

        for accepted_proposition in self.propositions.filter(decision=True):
            PollAnswer.objects.create(
                poll_question=poll_question,
                creation_user=creation_user,
                answer_text=accepted_proposition.fiction.title,
            )

        self.open = False
        self.save()

        return poll

    def close_poll_and_select_winners(self, number_of_winners, **kwargs):
        """Clôt le sondage de sélection et sélectionne le nombre de vainqueurs"""

        modification_user = kwargs.pop("modification_user", None)

        assert self.poll

        # Si le sondage est toujours ouvert, on actualise sa date pour le fermer
        self.poll.poll.close_poll(modification_user=modification_user)

        results = self.poll.get_top_choices(number_of_top_choices=number_of_winners, flat_count=False)

        self.fictions.set(
            [Fiction.objects.get(title=result.answer_text) for result in results]
        )

        return self.fictions.all()


class Proposition(models.Model):
    """Modèle de proposition"""

    selection = models.ForeignKey(verbose_name="sélection",
                                  to="selections.Selection",
                                  on_delete=models.CASCADE,
                                  related_name="propositions",
                                  limit_choices_to={"open": True})
    fiction = models.ForeignKey(verbose_name="fiction",
                                to="fictions.Fiction",
                                on_delete=models.CASCADE,
                                related_name="+")
    proposed_by = models.ForeignKey(verbose_name="proposée par",
                                    to="users.User",
                                    on_delete=models.SET_NULL,
                                    related_name="+",
                                    null=True, blank=False)
    decision = models.BooleanField(verbose_name="décision",
                                   null=True, blank=False)
    decided_by = models.ForeignKey(verbose_name="décidée par",
                                   to="users.User",
                                   on_delete=models.SET_NULL,
                                   related_name="+",
                                   null=True, blank=False)
    comment = models.TextField(verbose_name="commentaire",
                               null=True, blank=False)

    class Meta:
        verbose_name = "proposition"
        constraints = [
            models.UniqueConstraint(
                fields=["selection", "fiction"],
                name="unique_fiction_per_selection",
            )
        ]

    def __str__(self):
        return "Proposition : " + self.fiction.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """Enregistre la proposition

            S'il s'agit d'une nouvelle proposition, échappe la vérification des informations concernant la décision.
            S'il s'agit d'une proposition existante, échappe la vérification de l'utilisateur proposant, en cas de
            suppression de cet utilisateur.
        """

        if self.id:
            self.full_clean(exclude=["proposed_by"])
        else:
            self.full_clean(exclude=["decision", "decided_by", "comment"])
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)