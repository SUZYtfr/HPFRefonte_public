from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.serializers import ModelSerializer, HiddenField, CurrentUserDefault, CreateOnlyDefault
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Selection, Proposition


class SelectionSerializer(ModelSerializer):

    class Meta:
        model = Selection
        fields = "__all__"


class SelectionViewSet(ReadOnlyModelViewSet):
    """Ensemble de vues pour les sélections"""

    queryset = Selection.objects.filter(open=True)
    serializer_class = SelectionSerializer


class CurrentSelectionDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["selection"]

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class PropositionSerializer(ModelSerializer):

    selection = HiddenField(default=CreateOnlyDefault(default=CurrentSelectionDefault()))
    proposed_by = HiddenField(default=CreateOnlyDefault(default=CurrentUserDefault()))

    class Meta:
        model = Proposition
        fields = ("selection", "proposed_by", "fiction",)


class PropositionCreationView(CreateAPIView):
    """Vue de création de proposition"""
    model = Proposition
    permission_classes = (IsAuthenticated,)
    serializer_class = PropositionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["selection"] = get_object_or_404(Selection, pk=self.kwargs["pk"])
        return context
