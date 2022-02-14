from rest_framework.serializers import *
from .models import PollGroup, PollQuestion, PollAnswer, Ballot
from django.conf import settings
from fictions.models import Chapter
from random import randint
from core.serializers import BaseModelSerializer


class CurrentPollQuestionDefault:
    """Renvoie la question de sondage contextuelle"""
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["poll_question"]

    def __repr__(self):
        return '%s()' % self.__class__.__name__


# TODO - chopage d'adresse IP
class CurrentIPAdresseDefault:
    """Renvoie l'adresse IP du visiteur votant"""

    requires_context = True

    def __call__(self, serializer_field):
        return ".".join([str(randint(0, 255)) for x in range(4)])

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class PollAnswerSerializer(BaseModelSerializer):
    """Sérialiseur de réponse de question de sondage"""

    class PollQuestionField(PrimaryKeyRelatedField):
        def get_queryset(self):
            return PollQuestion.objects.filter(
                creation_user=self.context["request"].user
            ).annotate(
                answer_count=models.Count("answers")
            ).filter(
                answer_count__lt=settings.MAX_POLL_ANSWERS
            )

    poll_question = PollQuestionField()

    class Meta:
        model = PollAnswer
        fields = ("id", "answer_text", "poll_question",
                  "creation_user", "creation_date", "modification_user", "modification_date",)


class PollQuestionSerializer(BaseModelSerializer):
    """Sérialiseur de question de sondage"""

    class ChapterField(PrimaryKeyRelatedField):
        def get_queryset(self):
            return Chapter.objects.filter(
                authors=self.context["request"].user,
                poll__isnull=True,
                validation_status=Chapter.ChapterValidationStage.PUBLISHED
            )

    chapter = ChapterField()

    class Meta:
        model = PollQuestion
        fields = ("id", "question_text",
                  "opening_datetime", "closing_datetime",
                  "members_only", "visibility",
                  "max_choices", "answers",
                  "chapter",
                  "creation_user", "creation_date", "modification_user", "modification_date",)
        read_only_fields = ("answers",)


class PollSerializer(BaseModelSerializer):
    """Sérialiseur de sondage"""

    questions = PollQuestionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = PollGroup
        fields = ("id", "title", "questions",
                  "creation_user", "creation_date", "modification_user", "modification_date",)


# TODO - Implémenter si on veut un vote pour un groupe de sondage
# class BulkBallotSerializer(ListSerializer):
#
#     def create(self, validated_data):
#         ballot = Ballot.objects.bulk_create(
#             user=validated_data[0].pop("user"),
#             ip_address=validated_data[0].pop("ip_address"),
#             poll=validated_data[0].pop("poll"),
#             vote_datetime=validated_data[0].pop("vote_datetime"),
#             choices_dict={data.pop("poll_question_id"): data.pop("choices") for data in validated_data}
#         )
#
#         return ballot
#
#     def to_representation(self, data):
#         return self.child.to_representation(data)


class BallotSerializer(ModelSerializer):
    """Sérialiseur de bulletin de votes"""

    # choices = ListField(write_only=True)

    class PollAnswerSelectionField(PrimaryKeyRelatedField):
        def get_queryset(self):
            return self.context["poll_question"].answers.all()

    choices = PollAnswerSelectionField(
        many=True,
        write_only=True,
        allow_empty=False,
    )

    user = HiddenField(default=CreateOnlyDefault(default=CurrentUserDefault()))
    poll_question = HiddenField(default=CreateOnlyDefault(default=CurrentPollQuestionDefault()))
    ip_address = HiddenField(default=CreateOnlyDefault(default=CurrentIPAdresseDefault()))
    vote_datetime = HiddenField(default=CreateOnlyDefault(default=timezone.now))

    def validate_choices(self, data):
        if len(set(data)) != len(data):
            raise ValidationError("Au moins un ID de réponse est dupliqué.")

        poll_question = self.context["poll_question"]

        if hasattr(poll_question, "selection") and len(data) != poll_question.answers.count():
            raise ValidationError("Tous les ID de réponses doivent être classés.")

        elif len(data) > poll_question.max_choices:
            raise ValidationError("La question a obtenu plus de réponses qu'autorisé.")

        return data

    def validate_vote_datetime(self, data):

        poll_question = self.context["poll_question"]

        if poll_question.opening_datetime >= data:
            raise ValidationError("Le sondage n'est pas encore ouvert.")
        elif poll_question.closing_datetime and (poll_question.closing_datetime <= data):
            raise ValidationError("Le sondage est clos.")

        return data

    class Meta:
        model = Ballot
        fields = ("poll_question", "choices", "user", "poll_question", "ip_address", "vote_datetime",)
        # list_serializer_class = BulkBallotSerializer


class ResultSerializer(ModelSerializer):

    class PollResultSerializer(ModelSerializer):

        class Meta:
            fields = ("id", "answer_text", "points",)
            model = PollAnswer

    answers = PollResultSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = PollQuestion
        fields = ("answers",)
