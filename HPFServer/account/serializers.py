from django.db import transaction
from rest_framework import serializers

from users.models import User
from users.serializers import (
    UserProfileSerializer,
    UserPreferencesSerializer,
)


class AccountCreationSerializer(serializers.ModelSerializer):
    preferences = UserPreferencesSerializer(required=False)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
           "id",
            "username",
            "password",
            "email",
            "profile",
            "preferences",
        ]
        extra_kwargs = {
            "username": {
                "read_only": False,
                "required": True,
            },
            "password": {
                "write_only": True,
                "allow_null": True,
                "min_length": 8,
                "max_length": 20,
            },
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class AccountManagementSerializer(AccountCreationSerializer):
    class Meta(AccountCreationSerializer.Meta):
        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
                "allow_null": True,
                "min_length": 8,
                "max_length": 20,
            },
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        modification_user = validated_data.get("modification_user")

        if password := validated_data.pop("password", None):
            instance.set_password(password)

        if profile_validated_data := validated_data.pop("profile", {}):
            profile_validated_data["modification_user"] = modification_user
            super().update(instance.user_profile, profile_validated_data)
        if preferences_validated_data := validated_data.pop("preferences", {}):
            super().update(instance.user_preferences, preferences_validated_data)

        return super().update(instance, validated_data)
