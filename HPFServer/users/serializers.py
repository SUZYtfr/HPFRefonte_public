from django.conf import settings
from rest_framework import serializers
from drf_extra_fields import fields as extra_fields

from core.serializers import ListableModelSerializer
from .models import (
    User,
    UserProfile,
    UserPreferences,
    ExternalProfile,
)
from images.serializers import ContentImageSerializer


class UserStatsSerializer(serializers.ModelSerializer):
    """Sérialiseur de statistiques d'utilisateur"""

    # review_drafts_left = serializers.SerializerMethodField()

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
            # "review_drafts_left",
        ]

    # def get_review_drafts_left(self, obj) -> int:
    #     if obj.has_perm("reviews.extra_review_drafts"):
    #         base_drafts = settings.PREMIUM_MAX_REVIEW_DRAFTS
    #     else:
    #         base_drafts = settings.MEMBERS_MAX_REVIEW_DRAFTS
    #     return base_drafts - obj.created_reviews.filter(draft=True).count()


class UserPreferencesSerializer(serializers.ModelSerializer):
    """Sérialiseur de préférences d'utilisateur"""

    class Meta:
        model = UserPreferences
        fields = [
            "font",
            "font_size",
            "line_spacing",
            "color_scheme",
            "color_scheme_in_reader",
            "skin",
            "show_animations",
            "show_profile_pictures",
            # "show_reaction",
            "member_review_policy",
            "anonymous_review_policy",
            "letter_spacing",
            "paragraph_spacing",
            "redirect_to_summary",
            "show_trigger_warnings",
            "show_review_editor",
            "email_for_review",
            "email_for_reply",
            "email_for_news",
            "email_for_favorite_activity",
            "email_for_favorite",
            "email_for_chapter_status",
            "result_order",
        ]


class ExternalProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalProfile
        fields = [
            "id",
            "website_type",
            "username",
            "is_visible",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur de profil d'utilisateur"""

    external_profiles = ExternalProfileSerializer(
        many=True,
        read_only=True,
    )
    bio_images = ContentImageSerializer(
        many=True,
        max_length=1,
        required=False,
        max_dimensions=(700, None),
    )

    # FIXME - branchement
    # profile_picture = ProfilePictureSerializer(required=False)
    profile_picture = extra_fields.Base64ImageField(
        source="profile_picture.src_path",
        required=False,
        allow_null=True,
    )
    banner = extra_fields.Base64ImageField(
        source="banner.src_path",
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = [
            "realname",  # if pref_showname ?
            "birthdate",  # if pref_showbirthdate ?
            "gender",  # if pref_showgender ?
            "bio",
            "bio_images",
            "external_profiles",
            "profile_picture",
            "banner",
            "age_consent",
        ]

    # FIXME - temporaire branchement
    def get_user_links(self, obj):
        return []


class UserCardSerializer(serializers.ModelSerializer):
    """
    Sérialiseur du lien vers une présentation d'utilisateur
    
    Comme on veut seulement la photo de profil en plus, sans le reste du profil,
    un sérialiseur imbriqué fait l'intermédiaire.
    """
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile",
        ]
    
    class UserProfilePictureSerializer(serializers.Serializer):
        profile_picture = extra_fields.Base64ImageField(
            source="profile_picture.src_path",
            allow_null=True,
        )

    profile = UserProfilePictureSerializer()


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

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_seen",
            "last_login",
            "profile",
            "stats",
        ]
        list_serializer_child_class = UserListSerializer
