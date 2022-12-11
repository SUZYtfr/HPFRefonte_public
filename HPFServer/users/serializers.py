from rest_framework import serializers

from django.conf import settings

from .models import User, UserProfile, UserPreferences, UserLink
from images.serializers import ProfilePictureSerializer, BannerSerializer
from core.serializers import ListableModelSerializer

from random import randint


class UserStatsSerializer(serializers.ModelSerializer):
    """Sérialiseur de statistiques d'utilisateur"""

    review_drafts_left = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "fiction_count",
            "chapter_count",
            "collection_count",
            "review_count",
            "read_count",
            "word_count",
            "comment_count",
            "review_reply_count",
            "review_drafts_left",
        ]

    def get_review_drafts_left(self, obj) -> int:
        if obj.has_perm("reviews.extra_review_drafts"):
            base_drafts = settings.PREMIUM_MAX_REVIEW_DRAFTS
        else:
            base_drafts = settings.MEMBERS_MAX_REVIEW_DRAFTS
        return base_drafts - obj.created_reviews.filter(draft=True).count()


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Sérialiseur de préférences d'utilisateur"""

    class Meta:
        model = UserPreferences
        fields = [
            "age_consent",
            "font",
            "font_size",
            "line_spacing",
            "dark_mode",
            "skin",
            "show_reaction",
            "member_review_policy",
            "anonymous_review_policy",
        ]


class UserLinkSerializer(serializers.ModelSerializer):
    link_type_id = serializers.SerializerMethodField()

    class Meta:
        model = UserLink
        fields = [
            "display_text",
            "link_type_id",
            "url",
        ]

    def get_link_type_id(self, obj):
        return randint(1,6)


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur de profil d'utilisateur"""

    user_links = UserLinkSerializer(many=True, read_only=True)
    avatar = ProfilePictureSerializer(
        source="profile_picture",
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "avatar",
            "user_links",
            "realname",  # if pref_showname ?
            "birthdate",  # if pref_showbirthdate ?
            "gender",  # if pref_showgender ?
            # "email"# if pref_showemail?
        ]


class UserCardSerializer(serializers.ModelSerializer):
    """Sérialiseur du lien vers une présentation d'utilisateur"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]


class UserSerializer(ListableModelSerializer):
    """Sérialiseur d'utilisateur"""

    profile = UserProfileSerializer(required=False)
    stats = UserStatsSerializer(read_only=True, source="*")
    banner = BannerSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "nickname",
            "password",
            "email",
            "first_seen",
            "last_login",
            "profile",
            "stats",
            "banner",
        ]
        list_serializer_child_class = UserListSerializer
        extra_kwargs = {
            "nickname": {"write_only": True},
        }
