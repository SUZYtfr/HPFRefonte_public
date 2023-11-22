from django.db.transaction import atomic
from rest_framework.serializers import ModelSerializer, CharField, ListField
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from rest_framework_recursive.fields import RecursiveField
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import (
    BaseReview,
    FictionReview,
    ChapterReview,
    CollectionReview,
)
from core.serializers import ListableModelSerializer

"""
TODO - corriger le schema pour faire apparaître FictionCardSerializer par ex.
"""

class BaseReviewSerializer(ModelSerializer):
    class Meta:
        fields = [
            "id",
            "text",
            "is_draft",
            "is_archived",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "publication_date",
            # "as_staff",
        ]
        # extra_kwargs = {
        #     "is_draft": {"write_only": True},
        # }
        # list_serializer_child_class = ReviewListSerializer

    text = CharField(allow_blank=False, style={"base_template": "textarea.html"})
    creation_user = PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    modification_user = PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    # as_staff = serializers.HiddenField(default=False, label="Publication par le compte de modération", write_only=True)

    # def validate(self, attrs):
    #     if attrs.get("as_staff") and attrs.get("is_draft"):
    #         raise serializers.ValidationError("Une review par le compte de modération ne peut pas avoir de brouillon.")
    #     return attrs


class ReviewReplySerializer(BaseReviewSerializer):
    """Sérialiseur de réponse à review"""

    class Meta(BaseReviewSerializer.Meta):
        model = BaseReview
        fields = BaseReviewSerializer.Meta.fields + [
            "replies",
        ]

    replies = ListField(
        source="get_children",
        read_only=True,
        child=RecursiveField(),
    )


class FictionReviewSerializer(BaseReviewSerializer):
    class Meta(BaseReviewSerializer.Meta):
        model = FictionReview
        fields = BaseReviewSerializer.Meta.fields + [
            "grading",
            "fiction",
            "fiction_id",
        ]
        extra_kwargs = {
            "fiction_id": {
                "write_only": True,
                "source": "fiction",
            },
        }

    fiction = PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.FictionCardSerializer",
    )


class ChapterReviewSerializer(BaseReviewSerializer):
    class Meta(BaseReviewSerializer):
        model = ChapterReview
        fields = BaseReviewSerializer.Meta.fields + [
            "grading",
            "chapter",
            "chapter_id",
            # "parent_fiction",
        ]
        extra_kwargs = {
            "chapter_id": {
                "write_only": True,
                "source": "chapter",
            },
        }

    chapter = PresentablePrimaryKeyRelatedField(
        read_only=True,
        presentation_serializer="fictions.serializers.ChapterCardSerializer",
    )
    # parent_fiction = FictionSerializer(source="chapter.fiction")


class CollectionReviewSerializer(BaseReviewSerializer):
    class Meta(BaseReviewSerializer.Meta):
        model = CollectionReview
        fields = BaseReviewSerializer.Meta.fields + [
            "grading",
            "collection",
            "collection_id",
        ]
        extra_kwargs = {
            "collection_id": {
                "write_only": True,
                "source": "collection",
            },
        }

    collection = PresentablePrimaryKeyRelatedField(
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
