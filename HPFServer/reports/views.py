from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import Report
from .serializers import ReportSerializer


class ReportCreateView(CreateAPIView):
    """Vue de création de signalements"""

    permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        report_object = ContentType.objects.get(model=self.kwargs["contenttype"]).get_object_for_this_type(pk=self.kwargs["pk"])

        serializer.save(
            creation_user=self.request.user,
            creation_date=timezone.now(),
            object = report_object,
        )
