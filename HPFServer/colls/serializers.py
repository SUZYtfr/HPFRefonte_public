from django.shortcuts import get_object_or_404

from rest_framework import serializers
from drf_extra_fields import relations as extra_relations

from core.serializers import ListableModelSerializer

from .models import Collection
from fictions.models import Chapter


class CollectionChapterOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ("order",)

    order = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
    )

    def validate_order(self, value):

        if not len(set(value)) == len(value):
            raise serializers.ValidationError("Des ID de chapitres sont manquants ou en double.")

        if not set(self.instance.chapters.values_list("pk", flat=True)) == set(value):
            raise serializers.ValidationError("Les ID de chapitres passés ne correspondent pas aux ID existants.")

        return value

    def reorder(self):
        self.instance.set_work_order(self.validated_data["get_work_order"])


class MyCollectionChapterChoiceRelatedField(serializers.PrimaryKeyRelatedField):
    """Champ de choix de chapitre pour le sérialiseur de série"""

    queryset = Chapter.objects.filter(validation_status=7).order_by("fiction", "_order")

    def to_internal_value(self, data):
        """Recherche et renvoie un chapitre par son ID en vérifiant le statut de validation de sa fiction"""

        return get_object_or_404(Chapter, id=data[0], validation_status=7)

    def display_value(self, instance):
        """Renvoie le titre raccourci de la fiction, puis le titre du chapitre pour l'affichage des choix"""

        return f"{instance.fiction.title[:25]} : {instance.title}"


class CollectionCardSerializer(serializers.ModelSerializer):
    """Sérialiseur de carte de série"""

    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
        ]


class CollectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
        ]


class CollectionSerializer(ListableModelSerializer):
    """Sérialiseur de série"""

    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    modification_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )

    class Meta:
        model = Collection
        fields = (
            "id",
            "title",
            "summary",
            "status",
            "review_count",
            "mean",
            "fiction_count",
            "creation_user",
            "modification_user",
            "creation_date",
            "modification_date",
        )
        list_serializer_child_class = CollectionListSerializer


    # TODO - Repenser ceci : peut-être ne pas obliger le passage de chapitres lors de la création
    # du modèle Collection ? Mais alors comment garantir l'ordonnement des chapitres si la méthode
    # .create() de base se base sur Collection.set() ?
    # def create(self, validated_data):
    #     """Crée la série depuis les informations du sérialiseur validées
    #
    #         Le comportement normal de DRF consiste à créer d'abord l'instance de Collection, puis
    #         à ajouter les relations M2M.
    #         Ce comportement est évité ici. "chapters" est récupéré avant d'être traité comme M2M,
    #         et est "forcé" dans les attributs à passer à Collection.create().
    #         Pas très beau, mais permet de garantir l'ordonnement des chapitres par la table intermédiaire.
    #     """
    #     chapters = validated_data.pop("chapters")
    #     validated_data["starting_chapters"] = chapters
    #     return super().create(validated_data)


    # def update(self, instance, validated_data):
    #     """Met à jour la série depuis les informations du sérialiseur validées,
    #
    #         cf.: Méthode de création du sérialiseur de création
    #     """
    #
    #     chapters = validated_data.pop("chapters")
    #     instance.chapters.clear()
    #     instance.add_chapters(chapters)
    #
    #     return super().update(instance, validated_data)
