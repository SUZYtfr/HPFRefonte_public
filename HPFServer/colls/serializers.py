from django.shortcuts import get_object_or_404

from rest_framework.serializers import *

from .models import Collection
from fictions.models import Chapter

from core.serializers import BaseModelSerializer


class CollectionChapterOrderSerializer(ModelSerializer):

    class Meta:
        model = Collection
        fields = ("order",)

    order = ListField(
        child=IntegerField(),
        write_only=True,
    )

    def validate_order(self, value):

        if not len(set(value)) == len(value):
            raise ValidationError("Des ID de chapitres sont manquants ou en double.")

        if not set(self.instance.chapters.values_list("pk", flat=True)) == set(value):
            raise ValidationError("Les ID de chapitres passés ne correspondent pas aux ID existants.")

        return value

    def reorder(self):
        self.instance.set_work_order(self.validated_data["get_work_order"])


# SÉRIALISEURS PUBLIQUES

class CollectionBaseSerializer(BaseModelSerializer):

    class Meta:
        model = Collection
        fields = "__all__"


class CollectionCardSerializer(CollectionBaseSerializer):
    """Sérialiseur publique de carte de série """

    class Meta(CollectionBaseSerializer):
        fields = (
            "id",
            "title",
            "authors",
        )


class CollectionSerializer(CollectionBaseSerializer):
    """Sérialiseur de série publique"""

    reviews_url = HyperlinkedIdentityField(
        view_name="reviews:collection-reviews",
        lookup_field="pk",
        lookup_url_kwarg="pk",
    )

    class Meta:
        model = Collection
        fields = (
            "id",
            "title",
            "summary",
            "status",
            "creation_user",
            "modification_user",
            "creation_date",
            "modification_date",
            "authors",
            "chapters",
        )


class MyCollectionCardSerializer(CollectionBaseSerializer):
    """Sérialiseur privé de carte de série"""

    class Meta(CollectionBaseSerializer.Meta):
        fields = (
            "id",
            "title",
        )


class MyCollectionChapterChoiceRelatedField(PrimaryKeyRelatedField):
    """Champ de choix de chapitre pour le sérialiseur privé de série"""

    queryset = Chapter.objects.filter(validation_status=7).order_by("fiction", "_order")

    def to_internal_value(self, data):
        """Recherche et renvoie un chapitre par son ID en vérifiant le statut de validation de sa fiction"""

        return get_object_or_404(Chapter, id=data[0], validation_status=7)

    def display_value(self, instance):
        """Renvoie le titre raccourci de la fiction, puis le titre du chapitre pour l'affichage des choix"""

        return f"{instance.fiction.title[:25]} : {instance.title}"


class MyCollectionSerializer(CollectionBaseSerializer):
    """Sérialiseur privé de série"""

    chapters = MyCollectionChapterChoiceRelatedField(many=True)

    class Meta(CollectionBaseSerializer.Meta):
        fields = (
            "id",
            "title",
            "authors",
            "chapters",
            "summary",
            "status",
        )
        extra_kwargs = {
            "authors": {"read_only": True}
        }

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
