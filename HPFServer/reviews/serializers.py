from rest_framework.serializers import *

from reviews.models import Review, ReviewReply, ReviewTextVersion


class ReviewReplySerializer(ModelSerializer):
    """Sérialiseur de réponse à review"""

    as_staff = HiddenField(default=False, write_only=True)

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


class StaffReviewReplySerializer(ReviewReplySerializer):
    as_staff = HiddenField(default=True, write_only=True)


class ReviewSerializer(ModelSerializer):
    """Sérialiseur publique de review"""

    content_type = StringRelatedField(source="content_type.name")
    text = CharField(allow_blank=False, style={'base_template': 'textarea.html'})
    replies = ReviewReplySerializer(read_only=True, many=True)
    as_staff = HiddenField(default=False, label="Publication par le compte de modération", write_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "content_type",
            "object_id",
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

    def validate(self, attrs):
        if attrs.get("as_staff") and attrs.get("draft"):
            raise ValidationError("Une review par le compte de modération ne peut pas avoir de brouillon.")
        return attrs

    def create(self, validated_data):
        text = validated_data.pop("text")
        instance = super().create(validated_data)

        instance.create_text_version(
            text=text,
            creation_user=validated_data["creation_user"],
            touch=False,
        )
        return instance

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


class StaffReviewSerializer(ReviewSerializer):
    """Sérialiseur de review de modérateur"""

    as_staff = BooleanField(default=False, label="Publication par le compte de modération", write_only=True)


class AnonymousReviewSerializer(ReviewSerializer):
    """Sérialiseur de review anonyme"""

    email = EmailField(write_only=True, label="adresse e-mail")
    as_staff = BooleanField(default=False, label="Publication par le compte de modération", write_only=True)
    draft = HiddenField(default=False)

    class Meta(ReviewSerializer.Meta):
        fields = ReviewSerializer.Meta.fields + ["email"]


class ReviewCardSerializer(ReviewSerializer):
    """Sérialiseur de carte de review"""

    reply_count = SerializerMethodField()

    class Meta(ReviewSerializer.Meta):
        pass

    def get_reply_count(self, obj):
        """Renvoie le compte de réponses à reviews"""

        return obj.replies.count()


class ReviewTextSerializer(ModelSerializer):

    class Meta:
        exclude = (
            "id",
            "review",
        )
        model = ReviewTextVersion
