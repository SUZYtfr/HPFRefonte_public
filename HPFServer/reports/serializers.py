from rest_framework.serializers import *

from django.utils import timezone

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

    def create(self, validated_data):
        validated_data["report_user"] = self.context["request"].user
        validated_data["datetime"] = timezone.now()
        validated_data["object"] = self.context["object"]

        return super().create(validated_data)
