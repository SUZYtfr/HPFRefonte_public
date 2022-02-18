from rest_framework.serializers import *

from .models import Report


class ReportSerializer(ModelSerializer):
    """Sérialiseur de signalement"""

    class Meta:
        model = Report
        fields = (
            "element",
            "datetime",
            "argument",
            "status",
        )
        read_only_fields = (
            "status",
            "datetime",
        )
