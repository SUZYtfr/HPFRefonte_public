from django.db import transaction
from rest_framework import serializers, exceptions
from drf_extra_fields import relations as extra_relations

from .models import Fiction, Chapter, Collection
from core.serializers import ListableModelSerializer
from users.serializers import UserCardSerializer
from images.models import ContentImage
from images.serializers import ContentImageSerializer
from characteristics.models import Characteristic, CharacteristicType


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
        fields = [
            "id",
            "title",
            "summary",
            "access",
            "review_count",
            "average",
            "creation_user",
            "modification_user",
            "creation_date",
            "modification_date",
        ]
        read_only_fields = [
            "average",
            "review_count",
            "creation_user",
            "modification_user",
            "creation_date",
            "modification_date",
        ]
        list_serializer_child_class = CollectionListSerializer


class FirstChapterSerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        required=True,
        write_only=True,
    )
    text_images = ContentImageSerializer(
        many=True,
        required=False,
        write_only=True,
    )

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "startnote",
            "endnote",
            "text",
            "text_images",
            "trigger_warnings",
        ]
        extra_kwargs = {
            "startnote": {
                "write_only": True,
            },
            "endnote": {
                "write_only": True,
            },
        }


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
    authors = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        many=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    series = CollectionCardSerializer(
        read_only=True,
        many=True,
    )

    summary_images = ContentImageSerializer(
        many=True,
        max_length=1,
        required=False,
    )

    first_chapter = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.ChapterCardSerializer",
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
            "first_chapter",
        ]


class FictionSerializer(ListableModelSerializer):
    """Sérialiseur privé de fiction"""

    characteristics = extra_relations.PresentablePrimaryKeyRelatedField(
        many=True,
        queryset=Characteristic.objects.allowed(),
        presentation_serializer="characteristics.serializers.CharacteristicCardSerializer",
    )
    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    authors = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        many=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    # TODO - renommer franchement en collections, faire sauter read_only
    series = extra_relations.PresentablePrimaryKeyRelatedField(
        many=True,
        read_only=True,
        presentation_serializer="fictions.serializers.CollectionCardSerializer",
    )
    first_chapter = FirstChapterSerializer(
        required=True,
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
            # "coauthors",
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
            "first_chapter",
            "member_review_policy",
            "anonymous_review_policy",
        ]
        read_only_fields = [
            # "coauthors",
            "word_count",
            "average",
            "status",
            "read_count",
            "chapters",
            "featured",
            "creation_date",
            "creation_user",
            "modification_date",
            "modification_user",
        ]
        list_serializer_child_class = FictionListSerializer

    def validate_characteristics(self, value):
        """
        Valide les caractéristiques données pour la création de la fiction
        
        Compte le nombre de caractéristiques données dans chaque type de caractéristiques.
        Compare ce compte avec les bornes de chaque type de caractéristiques.
        """

        characteristic_types = CharacteristicType.objects.open().values("id", "min_limit", "max_limit")
        chartype_ids = [characteristic.characteristic_type_id for characteristic in set(value)]
        chartype_counts = {chartype_id: chartype_ids.count(chartype_id) for chartype_id in set(chartype_ids)}

        errors = []

        for characteristic_type in characteristic_types:
            characteristic_type_id = characteristic_type["id"]
            chartype_count = chartype_counts.get(characteristic_type_id, 0)
            min_limit = characteristic_type["min_limit"]
            max_limit = characteristic_type["max_limit"] or float("inf")
            if not (min_limit <= chartype_count <= max_limit):
                errors.append(f"chartype {characteristic_type_id} : {chartype_count} occurences (min {min_limit}, max {max_limit})")

        if errors:
            errors = "\n".join(errors)
            msg = f"Vérifier le nombre de caractéristiques :\n{errors}"
            raise exceptions.ValidationError(msg)
 
        return value

    @transaction.atomic
    def create(self, validated_data):
        """Les infos du premier chapitre sont imbriquées"""

        summary_images = validated_data.pop("summary_images", None)

        first_chapter_validated_data = validated_data.pop("first_chapter")
        text_images = first_chapter_validated_data.pop("text_images", None)
        text = first_chapter_validated_data.pop("text")

        fiction = super().create(validated_data)

        if summary_images:
            images = [
                ContentImage(
                    **_hpf_image,
                    creation_user=validated_data["creation_user"],                
                ) for _hpf_image in summary_images
            ]
            images = ContentImage.objects.bulk_create(images)
            fiction.summary_images.set(images)
        
        trigger_warnings = first_chapter_validated_data.pop("trigger_warnings", None)
        chapter = Chapter(
            fiction=fiction,
            creation_user=fiction.creation_user,
            **first_chapter_validated_data,
        )
        chapter.save()
        chapter.trigger_warnings.set(trigger_warnings)
        chapter.create_text_version(
            creation_user_id=chapter.creation_user_id,
            text=text,
        )

        if text_images:
            images = [
                ContentImage(
                    **_hpf_image,
                    creation_user=validated_data["creation_user"],                
                ) for _hpf_image in text_images
            ]
            images = ContentImage.objects.bulk_create(images)
            chapter.text_images.set(images)

        return fiction


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
            "trigger_warnings",
            # "member_review_policy",
            # "anonymous_review_policy",
        ]
        read_only_fields = [
            "order",
            "validation_status",
            "read_count",
            "fiction",
            "creation_date",
            "creation_user",
            "modification_date",
            "modification_user",
        ]
        list_serializer_child_class = ChapterListSerializer


class ChapterCardSerializer(serializers.ModelSerializer):
    """Sérialiseur de carte de chapitre"""

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "order",
            "trigger_warnings",
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
            "storynote",
            "chapters",
        ]
