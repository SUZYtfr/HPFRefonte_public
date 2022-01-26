from rest_framework.serializers import ModelSerializer

from django.utils import timezone


class BaseModelSerializer(ModelSerializer):
    """Base de sérialiseur de modèle implémentant les champs automatiques de création et de mise à jour"""

    def create(self, validated_data):
        validated_data["creation_user"] = self.context["request"].user
        validated_data["creation_date"] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["modification_user"] = self.context["request"].user
        validated_data["modification_date"] = timezone.now()
        return super().update(instance, validated_data)
