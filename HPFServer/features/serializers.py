from rest_framework import serializers, exceptions

from .models import Feature, Category
from core.serializers import CardSerializer

class FeatureBaseSerializer(serializers.ModelSerializer):
    """Base pour les sérialiseurs de caractéristiques"""

    class Meta:
        model = Feature
        fields = "__all__"


class FeatureCardSerializer(CardSerializer, serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = [
            "id",
            "string",
            "category_id",
        ]


class FeatureSerializer(FeatureBaseSerializer):
    """Sérialiseur de caractéristique"""

    is_personal = serializers.HiddenField(default=True)
    fiction_count = serializers.IntegerField(default=None)

    class Meta(FeatureBaseSerializer.Meta):
        fields = [
            "id",
            "name",
            "category_id",
            "parent_id",
            "description",
            "is_personal",
            "order",
            "fiction_count",
        ]
        extra_kwargs = {
            "description": {"read_only": True},
            "category": {"queryset": Category.objects.open()},
            "parent": {"queryset": Feature.objects.allowed(),
                       "allow_null": True,
                       "initial": ""},
            "order": {"source": "_order"},
        }

    def get_fiction_count(self, obj):
        return obj.fiction_set.count()

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
    def save(self, upsert=False, **kwargs):
        validated_data = {**self.validated_data, **kwargs}

        if upsert:
            self.instance, created = self.get_or_create(validated_data)
            return self.instance, created
        else:
            return super().save(**kwargs)


class StaffFeatureSerializer(FeatureBaseSerializer):
    """Sérialiseur de caractéristique pour les modérateurs"""

    url = serializers.HyperlinkedIdentityField(view_name="features:feature-detail")

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


class StaffCategorySerializer(serializers.ModelSerializer):
    """Sérialiseur de catégorie pour les modérateurs"""

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "min_limit",
            "max_limit",
        ]

    def validate(self, attrs):
        if attrs["max_limit"] and (attrs["min_limit"] > attrs["max_limit"]):
            raise exceptions.ValidationError({
                "min_limit": "Le minimum ne peut pas être plus grand que le maximum.",
                "max_limit": "Le minimum ne peut pas être plus grand que le maximum."
            })
        return attrs


class StaffFeatureOrderSerializer(serializers.ModelSerializer):
    """Sérialiseur d'ordre de caractéristiques pour les modérateurs"""

    class Meta:
        model = Category
        fields = ("order",)

    order = serializers.ListField(
        child=serializers.IntegerField(),
        source="get_feature_order",
    )

    def validate_order(self, value):
        if not len(set(value)) == len(value):
            raise serializers.ValidationError("Des ID de caractéristiques sont en double.")

        if not set(self.instance.get_feature_order()) == set(value):
            raise serializers.ValidationError("Les ID de caractéristiques passés ne correspondent pas aux ID existants.")

        return value

    def reorder(self):
        self.instance.set_feature_order(self.validated_data["get_feature_order"])
