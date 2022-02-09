from rest_framework.serializers import *
from rest_framework.exceptions import ValidationError

from django.utils import timezone

from .models import Feature, Category
from core.serializers import BaseModelSerializer


class FeatureBaseSerializer(BaseModelSerializer):

    class Meta:
        model = Feature
        fields = "__all__"


class FeatureSerializer(FeatureBaseSerializer):
    """Sérialiseur de caractéristique"""

    is_personal = HiddenField(default=True)

    class Meta(FeatureBaseSerializer.Meta):
        fields = (
            "id",
            "name",
            "url",
            "category",
            "parent",
            "description",
            "is_personal",
        )
        extra_kwargs = {
            "description": {"read_only": True},
            "category": {"queryset": Category.objects.exclude(is_closed=True)},
            "parent": {"queryset": Feature.objects.exclude(is_forbidden=True),
                       "allow_null": True,
                       "initial": ""},
            "url": {"view_name": "features:feature-detail"},
        }

    def get_or_create(self, validated_data):
        """Crée ou retourne la caractéristique correspondant à un nom

        Si la caractéristique existe déjà, la renvoie.
        Si la caractéristique existe déjà et est remplacée, renvoie la caractéristique de remplacement
        Si la caractéristique existe déjà et est interdite sans remplacement, lance une erreur.
        """
        name = validated_data.pop("name")
        instance, created = self.Meta.model.objects.get_or_create(name=name, defaults=validated_data)
        if instance.is_forbidden:
            if instance.replace_with:
                return instance.replace_with, created
            raise NameError("Ce tag est interdit")
        return instance, created

    # Ceci est une réécriture, penser aux conséquences de laisser à côté les vérifications faites par Django !
    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}

        if self.instance is not None:
            validated_data["modification_user"] = self.context["request"].user
            validated_data["modification_date"] = timezone.now()
            self.instance = self.update(self.instance, validated_data)
        else:
            validated_data["creation_user"] = self.context["request"].user
            validated_data["creation_date"] = timezone.now()
            self.instance, created = self.get_or_create(validated_data)
            if created:
                self.created = True  # Capté par la vue correspondante pour changer le code HTTP
        return self.instance


class StaffFeatureSerializer(FeatureBaseSerializer):
    """Sérialiseur de caractéristique pour les modérateurs"""

    url = HyperlinkedIdentityField(view_name="features:feature-detail")

    class Meta(FeatureBaseSerializer.Meta):
        pass

    def save(self, **kwargs):
        """Enregistre la caractéristique

        Si la caractéristique est mise à jour et est indiquée comme interdite, appelle sa fonction ban()."""
        validated_data = {**self.validated_data, **kwargs}

        if self.instance and validated_data["is_forbidden"]:
            self.instance.ban(
                modification_user=self.context["request"].user,
                replace_with=validated_data["replace_with"])
            return self.instance

        return super().save(**kwargs)


class StaffCategorySerializer(BaseModelSerializer):
    """Sérialiseur de catégorie pour les modérateurs"""

    class Meta:
        model = Category
        fields = "__all__"

    def validate(self, attrs):
        if attrs["max_limit"] and (attrs["min_limit"] > attrs["max_limit"]):
            raise ValidationError({
                "min_limit": "Le minimum ne peut pas être plus grand que le maximum.",
                "max_limit": "Le minimum ne peut pas être plus grand que le maximum."
            })
        return attrs


class StaffFeatureOrderSerializer(BaseModelSerializer):
    """Sérialiseur d'ordre de caractéristiques pour les modérateurs"""

    class Meta:
        model = Category
        fields = ("order",)

    order = ListField(
        child=IntegerField(),
        source="get_feature_order",
    )

    def validate_order(self, value):

        if not len(set(value)) == len(value):
            raise ValidationError("Des ID de caractéristiques sont en double.")

        if not set(self.instance.get_feature_order()) == set(value):
            raise ValidationError("Les ID de caractéristiques passés ne correspondent pas aux ID existants.")

        return value

    def reorder(self):
        self.instance.set_feature_order(self.validated_data["get_feature_order"])
