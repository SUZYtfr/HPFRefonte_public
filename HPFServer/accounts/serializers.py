from rest_framework.serializers import ModelSerializer

from users.models import User, UserProfile
from users.serializers import UserPreferencesSerializer
from images.serializers import ProfilePictureSerializer


class ProfileSerializer(ModelSerializer):
    avatar = ProfilePictureSerializer(
        source="profile_picture",
    )

    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "realname",
            "birthdate",
            "gender",
            "avatar",
        ]


class AccountCreationSerializer(ModelSerializer):
    """Sérialiseur de création de compte utilisateur"""

    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "email",
            "password",
            "profile",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "allow_null": False,
                "min_length": 8,
                "max_length": 20,
            },
        }

    def create(self, validated_data):
        profile_validated_data = validated_data.pop("profile", {})
        user = self.Meta.model.objects.create_user(**validated_data, **profile_validated_data)
        return user


class AccountManagementSerializer(ModelSerializer):
    """Sérialiseur de gestion de compte utilisateur"""

    profile = ProfileSerializer(required=False)
    preferences = UserPreferencesSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "nickname",
            "password",
            "email",
            "last_login",
            "is_active",
            "profile",
            "preferences",
        ]
        read_only_fields = [
            "nickname",
            "last_login",
            "is_active",
            "banner",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "allow_null": True,
                "min_length": 8,
                "max_length": 20,
            }
        }

    def update(self, instance, validated_data):
        modification_user = validated_data.get("modification_user")

        if password := validated_data.pop("password", None):
            instance.set_password(password)

        if profile_validated_data := validated_data.pop("profile", None):
            profile_validated_data["modification_user"] = modification_user
            super().update(instance.profile, profile_validated_data)
        if preferences_validated_data := validated_data.pop("preferences", None):
            super().update(instance.preferences, preferences_validated_data)

        return super().update(instance, validated_data)
