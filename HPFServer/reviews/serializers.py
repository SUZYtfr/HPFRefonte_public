from rest_framework.serializers import *

from fictions.serializers import FictionCardSerializer, Fiction, ChapterCardSerializer
from colls.serializers import CollectionCardSerializer, Collection
from fictions.models import Chapter
from users.serializers import UserCardSerializer

from users.models import User
from reviews.models import Review, ReviewReply, ReviewTextVersion
from core.models import get_moderation_account

from django.utils import timezone

from rest_framework.exceptions import PermissionDenied
from rest_framework.status import HTTP_403_FORBIDDEN


# RAR

class ReviewReplySerializer(ModelSerializer):
    """Sérialiseur de réponse à review"""

    class Meta:
        model = ReviewReply
        fields = "__all__"

    def create(self, validated_data):
        try:
            validated_data["parent"] = self.context["parent"]
        except KeyError:
            validated_data["review"] = self.context["review"]

        try:
            instance = super().create(validated_data)
        except PermissionError as e:
            raise PermissionDenied(
                code=HTTP_403_FORBIDDEN,
                detail=str(e),
            )

        return instance


# SÉRIALISEURS PUBLIQUES

class ReviewSerializer(ModelSerializer):
    """Sérialiseur publique de review"""

    replies = ReviewReplySerializer(read_only=True, many=True)
    reviewed_object = SerializerMethodField()
    text = CharField()

    class Meta:
        model = Review
        exclude = (
            "content_type",
            "object_id",
        )
        extra_kwargs = {
            "draft": {"write_only": True},
        }

    def create(self, validated_data):

        validated_data["work"] = self.context["work"]

        try:
            instance = super().create(validated_data)
        except PermissionError as e:
            raise PermissionDenied(
                code=HTTP_403_FORBIDDEN,
                detail=str(e),
            )

        return instance

    def get_reviewed_object(self, obj):
        """Renvoie le sérialiseur approprié au type d'élément reviewé"""

        serializer = {
            User: UserCardSerializer,
            Fiction: FictionCardSerializer,
            Chapter: ChapterCardSerializer,
            Collection: CollectionCardSerializer,
        }.get(type(obj.work))

        return serializer(obj.work, context=self.context).data


class AnonymousReviewSerializer(ReviewSerializer):
    """Sérialiseur de review anonyme"""

    email = EmailField(write_only=True, label="adresse e-mail")
    draft = HiddenField(default=False)

    class Meta(ReviewSerializer.Meta):
        pass

    def create(self, validated_data):
        try:
            creation_user = User.objects.get(
                email=validated_data["email"],
            )
        except User.DoesNotExist:
            creation_user = User(
                email=validated_data["email"],
            )
            creation_user.set_unusable_password()
            creation_user.save_base()  # outrepasse le full_clean

        validated_data["work"] = self.context["work"]
        validated_data["creation_user"] = creation_user
        validated_data["creation_date"] = timezone.now()

        try:
            instance = ModelSerializer.create(self, validated_data)
        except PermissionError as e:
            raise PermissionDenied(
                code=HTTP_403_FORBIDDEN,
                detail=str(e),
            )

        return instance


class StaffReviewSerializer(ReviewSerializer):
    """Sérialiseur de review de modérateur"""

    replies = ReviewReplySerializer(read_only=True, many=True)
    text = CharField()

    as_staff = BooleanField(default=False, label="Publication par le compte de modération", write_only=True)

    class Meta(ReviewSerializer.Meta):
        pass

    def validate(self, attrs):
        if attrs.get("as_staff") and attrs.get("draft"):
            raise ValidationError("Une review par le compte de modération ne peut pas avoir de brouillon.")
        return attrs

    def create(self, validated_data):
        if self.context["request"].user.has_perm("reviews.can_post_review_as_staff") and (validated_data["as_staff"] is True):
            creation_user = get_moderation_account()
        else:
            creation_user = self.context["request"].user

        validated_data["work"] = self.context["work"]
        validated_data["creation_user"] = creation_user
        validated_data["creation_date"] = timezone.now()

        try:
            instance = ModelSerializer.create(self, validated_data)
        except PermissionError as e:
            raise PermissionDenied(
                code=HTTP_403_FORBIDDEN,
                detail=str(e),
            )

        return instance


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
