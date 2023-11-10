from django.db import transaction
from rest_framework import serializers
from drf_extra_fields import relations as extra_relations
from rest_framework_recursive.fields import RecursiveField
from rest_polymorphic.serializers import PolymorphicSerializer

from reviews.models import (
    BaseReview,
    FictionReview,
    ChapterReview,
    CollectionReview,
)
from core.serializers import ListableModelSerializer


class ReviewReplySerializer(serializers.ModelSerializer):
    """Sérialiseur de réponse à review"""

    text = serializers.CharField(allow_blank=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = BaseReview
        fields = [
            "id",
            "text",
            "is_draft",
            "is_archived",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "replies",
            # "as_staff",
        ]
        # extra_kwargs = {
        #     "is_draft": {"write_only": True},
        # }
        # list_serializer_child_class = ReviewListSerializer

    replies = serializers.ListField(
        source="get_children",
        read_only=True,
        child=RecursiveField(),
    )

    text = serializers.CharField(
        allow_blank=False,
        style={"base_template": "textarea.html"},
    )
    # as_staff = serializers.HiddenField(default=False, label="Publication par le compte de modération", write_only=True)
    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )

    # def validate(self, attrs):
    #     if attrs.get("as_staff") and attrs.get("is_draft"):
    #         raise serializers.ValidationError("Une review par le compte de modération ne peut pas avoir de brouillon.")
    #     return attrs

    @transaction.atomic
    def create(self, validated_data):
        # if validated_data.pop("as_staff"):
        #     validated_data["creation_user"] = get_moderation_account()
        instance = self.Meta.model.objects.create(
            **validated_data,
        )
        return instance


class FictionReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = FictionReview
        fields = [
            "id",
            "fiction",
            "text",
            "grading",
            "is_draft",
            "is_archived",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
        ]

    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    fiction = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.FictionCardSerializer",
    )


class ChapterReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = ChapterReview
        fields = [
            "id",
            "chapter",
            # "parent_fiction",
            "text",
            "grading",
            "is_draft",
            "is_archived",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
        ]

    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    chapter = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.ChapterCardSerializer",
    )
    # chapter = ChapterSerializer()
    # parent_fiction = FictionSerializer(source="chapter.fiction")


class CollectionReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = CollectionReview
        fields = [
            "id",
            "collection",
            "text",
            "grading",
            "is_draft",
            "is_archived",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
        ]

    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    collection = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.CollectionCardSerializer",
    )


class AllReviewSerializer(PolymorphicSerializer):
    resource_type_field_name = "item_type"
    model_serializer_mapping = {
        CollectionReview: CollectionReviewSerializer,
        FictionReview: FictionReviewSerializer,
        ChapterReview: ChapterReviewSerializer,
        BaseReview: ReviewReplySerializer,
    }


'''
class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "reply_count",
            "grading",
            "creation_user",
            "creation_date",
        ]

    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )


class AnonymousReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(allow_blank=False, style={'base_template': 'textarea.html'})
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Review
        fields = [
            "text",
            "grading",
            "email",
        ]

    def create(self, validated_data):
        return self.Meta.model.objects.create_anonymous(**validated_data)


class ChapterAnonymousReviewSerializer(AnonymousReviewSerializer):
    class Meta:
        model = ChapterReview
        fields = [
            "text",
            "grading",
            "email",
            "chapter",
        ]


class FictionAnonymousReviewSerializer(AnonymousReviewSerializer):
    class Meta:
        model = FictionReview
        fields = [
            "text",
            "grading",
            "email",
            "fiction",
        ]


class CollectionAnonymousReviewSerializer(AnonymousReviewSerializer):
    class Meta:
        model = CollectionReview
        fields = [
            "text",
            "grading",
            "email",
            "collection",
        ]

class ChapterReviewListSerializer(ReviewListSerializer):
    class Meta(ReviewListSerializer.Meta):
        model = ChapterReview
        fields = ReviewListSerializer.Meta.fields + [
            "chapter",
        ]

    chapter = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.ChapterCardSerializer",
    )


class CollectionReviewListSerializer(ReviewListSerializer):
    class Meta(ReviewListSerializer.Meta):
        model = CollectionReview
        fields = ReviewListSerializer.Meta.fields + [
            "collection",
        ]

    collection = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.CollectionCardSerializer",
    )


class StaffReviewSerializer(ReviewSerializer):
    """Sérialiseur de review de modérateur"""

    as_staff = serializers.BooleanField(default=False, label="Publication par le compte de modération", write_only=True)


class AnonymousReviewSerializer(ReviewSerializer):
    """Sérialiseur de review anonyme"""

    email = serializers.EmailField(write_only=True, label="adresse e-mail")
    as_staff = serializers.BooleanField(default=False, label="Publication par le compte de modération", write_only=True)
    is_draft = serializers.HiddenField(default=False)

    class Meta(ReviewSerializer.Meta):
        fields = ReviewSerializer.Meta.fields + ["email"]

        
class ReviewCardSerializer(ReviewSerializer):
    """Sérialiseur de carte de review"""

    reply_count = serializers.SerializerMethodField()

    class Meta(ReviewSerializer.Meta):
        pass

    def get_reply_count(self, obj):
        """Renvoie le compte de réponses à reviews"""

        return obj.replies.count()
'''
