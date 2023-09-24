from django.db import transaction
from rest_framework import serializers
from drf_extra_fields import relations as extra_relations
from rest_framework_recursive.fields import RecursiveField

from reviews.models import (
    FictionReview,
    ChapterReview,
    CollectionReview,
)
from core.serializers import ListableModelSerializer


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


class ReviewSerializer(ListableModelSerializer):
    """Sérialiseur générique de review"""

    class Meta:
        fields = [
            "id",
            "text",
            "is_draft",
            "grading",
            "reply_count",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            # "as_staff",
        ]
        # extra_kwargs = {
        #     "is_draft": {"write_only": True},
        # }
        # list_serializer_child_class = ReviewListSerializer

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
        # text = validated_data.pop("text", "")
        instance = self.Meta.model.objects.create(
            **validated_data,
        )
        # instance.versions.create(text=text)
        return instance

    '''
    def update(self, instance, validated_data):
        text = validated_data.pop("text", None)
        instance = super().update(instance, validated_data)
        if text and text != instance.text:
            instance.create_text_version(
                text=text,
                creation_user=validated_data["modification_user"],
                touch=True
            )
        return instance
    '''


class ReviewReplySerializer(ListableModelSerializer):
    """Sérialiseur générique de réponse à review"""

    class Meta:
        fields = [
            "id",
            "text",
            "replies",
            "creation_user",
            "creation_date",
        ]

    text = serializers.CharField(
        allow_blank=False,
        style={"base_template": "textarea.html"},
    )
    replies = serializers.ListField(
        source="get_children",
        read_only=True,
        child=RecursiveField(),
    )
    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )

    @transaction.atomic
    def create(self, validated_data):
        # if validated_data.pop("as_staff"):
        #     validated_data["creation_user"] = get_moderation_account()
        # text = validated_data.pop("text", "")
        instance = self.Meta.model.objects.create(
            **validated_data,
        )
        # instance.versions.create(text=text)
        return instance

    '''
    def update(self, instance, validated_data):
        text = validated_data.pop("text", None)
        instance = super().update(instance, validated_data)
        if text and text != instance.text:
            instance.create_text_version(
                text=text,
                creation_user=validated_data["modification_user"],
                touch=True
            )
        return instance
    '''

'''
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
'''


class FictionReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = FictionReview
        fields = ReviewSerializer.Meta.fields + [
            "fiction",
        ]

    fiction = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.FictionCardSerializer",
    )


class FictionReviewReplySerializer(ReviewReplySerializer):
    class Meta(ReviewReplySerializer.Meta):
        model = FictionReview


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


class ChapterReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = ChapterReview
        fields = ReviewSerializer.Meta.fields + [
            "chapter",
        ]
    
    chapter = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.ChapterCardSerializer",
    )


class ChapterReviewReplySerializer(ReviewReplySerializer):
    class Meta(ReviewReplySerializer.Meta):
        model = ChapterReview


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


class CollectionReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = CollectionReview
        fields = ReviewSerializer.Meta.fields + [
            "collection",
        ]
    
    collection = extra_relations.PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.CollectionCardSerializer",
    )


class CollectionReviewReplySerializer(ReviewReplySerializer):
    class Meta(ReviewReplySerializer.Meta):
        model = CollectionReview


'''
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

        
class FictionReviewTextSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = (
            "id",
            "fiction_review",
        )
        model = FictionReviewTextVersion


class ChapterReviewTextSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = (
            "id",
            "chapter_review",
        )
        model = ChapterReviewTextVersion


class CollectionReviewTextSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = (
            "id",
            "collection_review",
        )
        model = CollectionReviewTextVersion
'''