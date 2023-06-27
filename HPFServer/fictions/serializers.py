from rest_framework import serializers, exceptions
from drf_extra_fields import relations as extra_relations

from characteristics.models import CharacteristicType, Characteristic
from users.serializers import UserCardSerializer
from core.serializers import ListableModelSerializer
from core.text_functions import read_text_file
from reviews.models import Review
from images.serializers import ContentImageSerializer

from .models import Fiction, Chapter, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
        ]


class FictionListSerializer(serializers.ModelSerializer):
    characteristics = extra_relations.PresentablePrimaryKeyRelatedField(
        many=True,
        read_only=True,
        presentation_serializer="characteristics.serializers.CharacteristicCardSerializer",
    )
    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    authors = serializers.SerializerMethodField()
    series = CollectionSerializer(read_only=True, many=True, source="collections")

    summary_images = ContentImageSerializer(
        many=True,
        max_length=1,
        required=False,
    )

    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
            "creation_user",
            "creation_date",
            "last_update_date",
            "average",
            "summary",
            "summary_images",
            "storynote",
            "status",
            "read_count",
            "word_count",
            "collection_count",
            "featured",
            "characteristics",
            "authors",
            "series",
            "chapter_count",
            "review_count",
        ]

    def get_authors(self, obj):
        author = obj.creation_user
        return [UserCardSerializer(instance=author).data]


class FictionSerializer(ListableModelSerializer):
    """Sérialiseur privé de fiction"""

    characteristics = extra_relations.PresentablePrimaryKeyRelatedField(
        many=True,
        read_only=True,
        presentation_serializer="characteristics.serializers.CharacteristicCardSerializer",
    )
    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    authors = serializers.SerializerMethodField()
    series = extra_relations.PresentablePrimaryKeyRelatedField(
        source="collections",
        many=True,
        read_only=True,
        presentation_serializer="fictions.serializers.CollectionCardSerializer",
    )
    member_review_policy = serializers.IntegerField(read_only=True, source="creation_user.preferences.member_review_policy")
    anonymous_review_policy = serializers.IntegerField(read_only=True, source="creation_user.preferences.anonymous_review_policy")

    summary_images = ContentImageSerializer(
        many=True,
        required=False,
    )

    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "coauthors",
            "last_update_date",
            "average",
            "summary",
            "summary_images",
            "storynote",
            "status",
            "read_count",
            "word_count",
            "collection_count",
            "featured",
            "characteristics",
            "authors",
            "series",
            "chapter_count",
            "review_count",
            "member_review_policy",
            "anonymous_review_policy",
        ]
        read_only_fields = (
            "coauthors",
            "word_count",
            "average",
            "status",
            "read_count",
            "chapters",
            "featured",
        )
        list_serializer_child_class = FictionListSerializer

    def get_authors(self, obj):
        author = obj.creation_user
        return [UserCardSerializer(instance=author).data]

    # def get_series(self, obj):
    #     collections = Collection.objects.filter(
    #         chapters__fiction=obj,
    #         chapters__validation_status=Chapter.ValidationStage.PUBLISHED,
    #     ).distinct()
    #     return CollectionSerializer(collections, many=True).data


    # characteristics = serializers.CharacteristicChoiceRelatedField(
    #     many=True,
    # )

    # reviews_url = serializers.HyperlinkedIdentityField(
    #     view_name="reviews:fictions:object-review-list",
    #     lookup_field="pk",
    #     lookup_url_kwarg="object_pk",
    # )

    def validate_characteristics(self, value):
        """Valide le nombre de caractéristiques pour chaque type"""

        characteristic_type_count = []

        for characteristic in value:
            characteristic_type_count.append(characteristic.characteristic_type.id)

        result = {"below_minimum": [], "above_maximum": []}
        for characteristic_type in CharacteristicType.objects.all():
            type_id_count = characteristic_type_count.count(characteristic_type.id)
            if type_id_count < characteristic_type.min_limit:
                result["below_minimum"].append(str(characteristic_type.min_limit - type_id_count) + " " + characteristic_type.name)
            if type_id_count > (characteristic_type.max_limit or float("inf")):
                result["above_maximum"].append(str(type_id_count - characteristic_type.max_limit) + " " + characteristic_type.name)

        below = ""
        above = ""

        if result["below_minimum"]:
            below = f"Sélectionner {', '.join(result['below_minimum'])} en plus."
        if result["above_maximum"]:
            above = f"Sélectionner {', '.join(result['above_maximum'])} en moins."

        if below or above:
            raise exceptions.ValidationError(" ".join([below, above]))

        return value


class FictionCardSerializer(serializers.ModelSerializer):
    """Sérialiseur de carte de fiction"""

    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
        ]


class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
        ]


class ChapterSerializer(ListableModelSerializer):
    """Sérialiseur de chapitre"""

    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    
    text_images = ContentImageSerializer(
        many=True,
        required=False,
    )

    # text = serializers.CharField(allow_blank=True, style={'base_template': 'textarea.html'})

    # member_review_policy = serializers.IntegerField(
    #     read_only=True,
    #     source="fiction.creation_user.preferences.member_review_policy",
    # )
    # anonymous_review_policy = serializers.IntegerField(
    #     read_only=True,
    #     source="fiction.creation_user.preferences.anonymous_review_policy",
    # )

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "fiction",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "startnote",
            "endnote",
            "order",
            "validation_status",
            "word_count",
            "read_count",
            "review_count",
            "average",
            "text",
            "text_images",
            # "reviews_url",
            # "member_review_policy",
            # "anonymous_review_policy",
        ]
        read_only_fields = (
            "order",
            "validation_status",
            "word_count",
            "read_count",
            "average",
            # "reviews_url",
            "fiction",
        )
        list_serializer_child_class = ChapterListSerializer

    def validate_text_file_upload(self, value):
        if value:
            try:
                return read_text_file(value)
            except Exception as e:
                raise exceptions.ValidationError(e)

    def validate(self, attrs):
        if not attrs.get("text"):
            if not attrs.get("text_file_upload"):
                raise exceptions.ValidationError("Le texte du chapitre doit être passé.")
            attrs.update({"text": attrs.get("text_file_upload")})
        attrs.pop("text_file_upload")
        return attrs

    def create(self, validated_data):
        text = validated_data.pop("text")
        instance = super().create(validated_data)
        instance.create_text_version(
            text=text,
            creation_user=self.context["request"].user,
            touch=False,
        )
        return instance

    def update(self, instance, validated_data):
        text = validated_data.pop("text")
        instance = super().update(instance, validated_data)
        instance.create_text_version(
            text=text,
            creation_user=self.context["request"].user,
            touch=True
        )
        return instance


class ChapterCardSerializer(serializers.ModelSerializer):
    """Sérialiseur de carte de chapitre"""

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "order",
        ]


class FictionTableOfContentsSerializer(serializers.ModelSerializer):
    """Sérialiseur de table des matières de fiction"""

    chapters = ChapterCardSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
            "chapters",
        ]


class FictionChapterOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fiction
        fields = ("order",)

    order = serializers.ListField(
        child=serializers.IntegerField(),
        source="get_chapter_order",
    )

    def validate_order(self, value):

        if not len(set(value)) == len(value):
            raise exceptions.ValidationError("Des ID de chapitres sont en double.")

        if not set(self.instance.get_chapter_order()) == set(value):
            raise exceptions.ValidationError("Les ID de chapitres passés ne correspondent pas aux ID existants.")

        return value

    def reorder(self):
        self.instance.set_chapter_order(self.validated_data["get_chapter_order"])



# class CollectionChapterOrderSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Collection
#         fields = ("order",)

#     order = serializers.ListField(
#         child=serializers.IntegerField(),
#         write_only=True,
#     )

#     def validate_order(self, value):

#         if not len(set(value)) == len(value):
#             raise serializers.ValidationError("Des ID de chapitres sont manquants ou en double.")

#         if not set(self.instance.chapters.values_list("pk", flat=True)) == set(value):
#             raise serializers.ValidationError("Les ID de chapitres passés ne correspondent pas aux ID existants.")

#         return value

#     def reorder(self):
#         self.instance.set_work_order(self.validated_data["get_work_order"])


# class MyCollectionChapterChoiceRelatedField(serializers.PrimaryKeyRelatedField):
#     """Champ de choix de chapitre pour le sérialiseur de série"""

#     queryset = Chapter.objects.filter(validation_status=7).order_by("fiction", "_order")

#     def to_internal_value(self, data):
#         """Recherche et renvoie un chapitre par son ID en vérifiant le statut de validation de sa fiction"""

#         return get_object_or_404(Chapter, id=data[0], validation_status=7)

#     def display_value(self, instance):
#         """Renvoie le titre raccourci de la fiction, puis le titre du chapitre pour l'affichage des choix"""

#         return f"{instance.fiction.title[:25]} : {instance.title}"


# class CollectionCardSerializer(serializers.ModelSerializer):
#     """Sérialiseur de carte de série"""

#     class Meta:
#         model = Collection
#         fields = [
#             "id",
#             "title",
#         ]


# class CollectionListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Collection
#         fields = [
#             "id",
#             "title",
#         ]


# class CollectionSerializer(ListableModelSerializer):
#     """Sérialiseur de série"""

#     creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
#         read_only=True,
#         presentation_serializer="users.serializers.UserCardSerializer",
#     )
#     modification_user = extra_relations.PresentablePrimaryKeyRelatedField(
#         read_only=True,
#         presentation_serializer="users.serializers.UserCardSerializer",
#     )

#     class Meta:
#         model = Collection
#         fields = (
#             "id",
#             "title",
#             "summary",
#             "status",
#             "review_count",
#             "average",
#             "fiction_count",
#             "creation_user",
#             "modification_user",
#             "creation_date",
#             "modification_date",
#         )
#         list_serializer_child_class = CollectionListSerializer


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
