from rest_framework import serializers
from drf_extra_fields import relations as extra_relations

from .models import Fiction, Chapter, Collection
from core.serializers import ListableModelSerializer
from users.serializers import UserCardSerializer
from images.serializers import ContentImageSerializer


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
    series = CollectionCardSerializer(
        read_only=True,
        many=True,
        source="collections",
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
    first_chapter = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.ChapterCardSerializer",
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
            "first_chapter",
            "member_review_policy",
            "anonymous_review_policy",
        ]
        read_only_fields = [
            "coauthors",
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

    def get_authors(self, obj):
        author = obj.creation_user
        return [UserCardSerializer(instance=author).data]


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

    def get_order(self, obj) -> int:
        return obj._order + 1  # index 0 -> 1

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
