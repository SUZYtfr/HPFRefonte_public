from users.serializers import UserSerializer, UserPreferencesSerializer


class AccountManagementSerializer(UserSerializer):
    preferences = UserPreferencesSerializer(required=False)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            "preferences",
        ]
        read_only_fields = [
            "last_login",
            "is_active",
            "banner",
        ]
        extra_kwargs = {
            "nickname": {
                "read_only": True,
            },
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


class AccountCreationSerializer(AccountManagementSerializer):
    class Meta(AccountManagementSerializer.Meta):
        extra_kwargs = {
            "nickname": {
                "required": True,
            },
        }

    def create(self, validated_data):
        profile_validated_data = validated_data.pop("profile", {})
        user = self.Meta.model.objects.create_user(**validated_data, **profile_validated_data)
        return user
