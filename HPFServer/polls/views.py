from django.utils import timezone

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import PollQuestion, PollAnswer
from .serializers import PollQuestionSerializer, BallotSerializer, ResultSerializer, PollAnswerSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


class PollViewSet(ReadOnlyModelViewSet):
    """Ensemble de vues de sondage"""

    serializer_class = PollQuestionSerializer
    queryset = PollQuestion.objects.filter(answers__gte=2).distinct()

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())


class MyPollViewSet(ModelViewSet):
    """Ensemble de vues privées de sondage"""

    permission_classes = (IsAuthenticated,)
    serializer_class = PollQuestionSerializer

    def get_queryset(self):
        return PollQuestion.objects.filter(creation_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())


class MyPollAnswerViewSet(ModelViewSet):
    """Ensemble de vues pricées de réponses de sondage"""

    permission_classes = (IsAuthenticated,)
    serializer_class = PollAnswerSerializer

    def get_queryset(self):
        return PollAnswer.objects.filter(creation_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creation_user=self.request.user, creation_date=timezone.now())

    def perform_update(self, serializer):
        serializer.save(modification_user=self.request.user, modification_date=timezone.now())


class VoteView(CreateAPIView):
    """Vue de création de votes"""

    serializer_class = BallotSerializer
    queryset = PollQuestion.objects.all()

    def check_object_permissions(self, request, obj):
        if obj.members_only and request.user.is_anonymous:
            self.permission_denied(request, "Le sondage est réservé aux membres.")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["poll_question"] = self.get_object()
        return context

    # TODO - peut-être impémenter ceci si réponse à un groupe de sondage.
    # def get_serializer(self, *args, **kwargs):
    #     if isinstance(kwargs.get("data", {}), list):
    #         kwargs["many"] = True
    #     return super().get_serializer(*args, **kwargs)


class ResultView(RetrieveAPIView):
    """Vue de résultats de sondage"""

    serializer_class = ResultSerializer
    queryset = PollQuestion.objects.all()

    def check_object_permissions(self, request, obj):
        if not obj.visibility and not (request.user == obj.creation_user):
            self.permission_denied(request, "Les résultats ne sont visibles que par l'auteur.")
        elif obj.members_only and request.user.is_anonymous:
            self.permission_denied(request, "Les résultats ne sont visibles que par les membres.")
