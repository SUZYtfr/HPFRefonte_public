from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType

from .models import Report
from .serializers import ReportSerializer


class ReportCreateView(CreateAPIView):
    """Vue de création de signalements"""

    permission_classes = (IsAuthenticated,)
    queryset = Report.objects
    serializer_class = ReportSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # L'objet est générique : il est récupéré par le biais de /signalement/<contenttype>/<pk>/ et envoyé au serialiseur
        context["object"] = ContentType.objects.get(model=self.kwargs["contenttype"]).get_object_for_this_type(pk=self.kwargs["pk"])

        return context
