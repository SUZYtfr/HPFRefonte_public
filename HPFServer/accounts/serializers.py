from rest_framework.serializers import Serializer, ModelSerializer, CharField,\
    ValidationError, api_settings

from users.models import User

from django.contrib.auth import authenticate


class PublicAccountCreationSerializer(ModelSerializer):
    """Sérialiseur d'informations de création d'un compte utilisateur"""

    class Meta:
        model = User
        fields = ("id", "nickname", "realname", "email", "password", "birthdate",)
        # write_only : aucune requête renvoyée ne contient le mdp par sécurité
        extra_kwargs = {"password": {"write_only": True,
                                     "min_length": 8,
                                     "max_length": 20}}

    def create(self, validated_data):
        """Crée le modèle User et le renvoie"""

        return self.Meta.model.objects.create_user(**validated_data)


class PrivateAccountManagementSerializer(ModelSerializer):
    """Sérialiseur d'informations de gestion de compte utilisateur"""

    class Meta:
        model = User
        fields = ("id", "nickname", "realname", "email", "birthdate",
                  "age_consent", "bio", "sex", "password",)
        extra_kwargs = {"password": {"write_only": True,
                                     "min_length": 8,
                                     "max_length": 20,
                                     "allow_null": True},
                        "nickname": {"read_only": True}}

    def update(self, instance, validated_data):
        """Met à jour l'objet User et le renvoie"""

        password = validated_data.pop("password")
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)

        user.save()

        return user


class PublicAccountLoginSerializer(Serializer):
    """Sérialiseur de jeton d'authentification"""

    nickname = CharField()
    password = CharField(style={"input_type": "password"},
                         trim_whitespace=False)

    def validate(self, attrs):
        """Authentifie et connecte un utilisateur"""

        nickname = attrs.get("nickname")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"),
                            username=nickname,
                            password=password)

        if not user:
            msg = "Le nom de compte et le mot de passe ne correspondent pas."
            raise ValidationError(msg, code="authentication")

        attrs["user"] = user
        return attrs
