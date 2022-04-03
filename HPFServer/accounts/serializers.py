from rest_framework.serializers import ModelSerializer

from users.models import User


class AccountCreationSerializer(ModelSerializer):
    """Sérialiseur de création de compte utilisateur"""

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "email",
            "password",
            "birthdate",
            "age_consent",
            "bio",
            "gender",
            "creation_date",
            "modification_date",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "allow_null": False,
                "min_length": 8,
                "max_length": 20,
            }
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = self.Meta.model.objects.create_user(**validated_data, password=None)
        user.set_password(password)
        return user


class AccountManagementSerializer(ModelSerializer):
    """Sérialiseur de gestion de compte utilisateur"""

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "password",
            "email",
            "birthdate",
            "age_consent",
            "bio",
            "gender",
            "creation_date",
            "user_pref_font",
            "user_pref_font_size",
            "user_pref_line_spacing",
            "user_pref_dark_mode",
            "user_pref_skin",
            "user_pref_show_reaction",
            "modification_date",
            "last_login",
            "is_active",
        ]
        read_only_fields = [
            "nickname",
            "last_login",
            "is_active",
            "mean",
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
        password = validated_data.pop("password", None)

        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)
