from rest_framework import serializers

from reviews.models import Review, ReviewReply, ReviewTextVersion, FictionReview, ChapterReview, CollectionReview
from core.serializers import ListableModelSerializer
from fictions.serializers import ChapterCardSerializer, FictionCardSerializer
from colls.serializers import CollectionCardSerializer
from users.serializers import UserCardSerializer
from core.utils import get_moderation_account


class ReviewReplyListSerializer(serializers.ModelSerializer):
    creation_user = UserCardSerializer()

    class Meta:
        model = ReviewReply
        fields = [
            "id",
            "creation_user",
            "creation_date",
            "text",
        ]


class ReviewReplySerializer(ListableModelSerializer):
    """Sérialiseur de réponse à review"""

    creation_user = UserCardSerializer()
    as_staff = serializers.HiddenField(default=False, write_only=True)

    class Meta:
        model = ReviewReply
        fields = [
            "id",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "review",
            "as_staff",
            "text",
        ]
        list_serializer_child_class = ReviewReplyListSerializer


class StaffReviewReplySerializer(ReviewReplySerializer):
    as_staff = serializers.HiddenField(default=True, write_only=True)


class ReviewListSerializer(serializers.ModelSerializer):
    creation_user = UserCardSerializer()

    class Meta:
        model = Review
        fields = [
            "id",
            "text",
            "reply_count",
            "grading",
            "creation_user",
            "creation_date",
        ]


class ReviewSerializer(ListableModelSerializer):
    """Sérialiseur publique de review"""

    text = serializers.CharField(allow_blank=False, style={'base_template': 'textarea.html'})
    replies = ReviewReplySerializer(read_only=True, many=True)
    as_staff = serializers.HiddenField(default=False, label="Publication par le compte de modération", write_only=True)
    creation_user = UserCardSerializer()

    class Meta:
        model = Review
        fields = [
            "id",
            "text",
            "replies",
            "draft",
            "grading",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "as_staff",
        ]
        extra_kwargs = {
            "draft": {"write_only": True},
        }
        list_serializer_child_class = ReviewListSerializer

    def validate(self, attrs):
        if attrs.get("as_staff") and attrs.get("draft"):
            raise serializers.ValidationError("Une review par le compte de modération ne peut pas avoir de brouillon.")
        return attrs

    def create(self, validated_data):
        # text = validated_data.pop("text")
        # instance = super().create(validated_data)
        # instance.create_text_version(
        #     text=text,
        #     creation_user=validated_data["creation_user"],
        #     touch=False,
        # )
        if validated_data.pop("as_staff"):
            validated_data["creation_user"] = get_moderation_account()
        instance = self.Meta.model.create(validated_data)
        return instance

    # def update(self, instance, validated_data):
        # text = validated_data.pop("text", None)
        # instance = super().update(instance, validated_data)
        # if text and text != instance.text:
        #     instance.create_text_version(
        #         text=text,
        #         creation_user=validated_data["modification_user"],
        #         touch=True
        #     )
        # return instance


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


class FictionReviewListSerializer(ReviewListSerializer):
    fiction = FictionCardSerializer()

    class Meta(ReviewListSerializer.Meta):

        fields = ReviewListSerializer.Meta.fields + [
            "fiction",
        ]


class FictionReviewSerializer(ReviewSerializer):
    fiction = FictionCardSerializer()

    class Meta(ReviewSerializer.Meta):
        model = FictionReview
        fields = ReviewSerializer.Meta.fields + [
            "fiction",
        ]
        list_serializer_child_class = FictionReviewListSerializer


class ChapterReviewListSerializer(ReviewListSerializer):
    chapter = ChapterCardSerializer()

    class Meta(ReviewListSerializer.Meta):
        fields = ReviewListSerializer.Meta.fields + [
            "chapter",
        ]


class ChapterReviewSerializer(ReviewSerializer):
    chapter = ChapterCardSerializer()

    class Meta(ReviewSerializer.Meta):
        model = ChapterReview
        fields = ReviewSerializer.Meta.fields + [
            "chapter",
        ]
        list_serializer_child_class = ChapterReviewListSerializer


class CollectionReviewListSerializer(ReviewListSerializer):
    collection = CollectionCardSerializer()

    class Meta(ReviewListSerializer.Meta):
        fields = ReviewListSerializer.Meta.fields + [
            "collection",
        ]


class CollectionReviewSerializer(ReviewSerializer):
    class Meta(ReviewSerializer.Meta):
        model = CollectionReview
        fields = ReviewSerializer.Meta.fields + [
            "collection",
        ]
        list_serializer_child_class = CollectionReviewListSerializer


class StaffReviewSerializer(ReviewSerializer):
    """Sérialiseur de review de modérateur"""

    as_staff = serializers.BooleanField(default=False, label="Publication par le compte de modération", write_only=True)


class AnonymousReviewSerializer(ReviewSerializer):
    """Sérialiseur de review anonyme"""

    email = serializers.EmailField(write_only=True, label="adresse e-mail")
    as_staff = serializers.BooleanField(default=False, label="Publication par le compte de modération", write_only=True)
    draft = serializers.HiddenField(default=False)

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


class ReviewTextSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = (
            "id",
            "review",
        )
        model = ReviewTextVersion
