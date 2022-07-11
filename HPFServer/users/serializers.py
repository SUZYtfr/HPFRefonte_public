from rest_framework import serializers

from .models import User, UserProfile, UserPreferences, UserLink
from core.serializers import ListableModelSerializer

from random import randint


class UserStatsSerializer(serializers.ModelSerializer):
    """Sérialiseur de statistiques d'utilisateur"""

    fiction_count = serializers.IntegerField(read_only=True, source="created_fictions.count")
    chapter_count = serializers.IntegerField(read_only=True, source="created_chapters.count")
    review_count = serializers.IntegerField(read_only=True, source="created_reviews.count")
    comment_count = serializers.IntegerField(read_only=True, source="created_comments.count")
    collection_count = serializers.IntegerField(read_only=True, source="created_collections.count")
    reviewreply_count = serializers.IntegerField(read_only=True, source="created_reviewreplys.count")
    # TODO - brouillons restants ?

    class Meta:
        model = User
        fields = [
            "fiction_count",
            "chapter_count",
            "review_count",
            "read_count",
            "word_count",
            "comment_count",
            "collection_count",
            "reviewreply_count",
        ]


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

    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "user_links",

            # realname if pref_showname ?
            # birthdate if pref_showbirthdate ?
            # gender if pref_showgender ?
            # email if pref_showemail?
        ]


class UserProfileStaffSerializer(UserProfileSerializer):
    email = serializers.CharField(source="user.email")

    class Meta(UserProfileSerializer.Meta):
        model = UserProfile
        fields = UserProfileSerializer.Meta.fields + [
            "realname",
            "birthdate",
            "gender",
            "email",
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
            # "url",
            "username",
        ]


class UserSerializer(ListableModelSerializer):
    """Sérialiseur d'utilisateur"""

    profile = UserProfileSerializer(read_only=True)
    stats = UserStatsSerializer(read_only=True, source="*")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile",
            "stats",
            "first_seen",
            "last_login",
            "banner",
        ]
        read_only_fields = [
            "banner",
        ]
        list_serializer_child_class = UserListSerializer


class UserStaffSerializer(UserSerializer):
    profile = UserProfileStaffSerializer(read_only=True)
