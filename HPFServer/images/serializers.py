from django.core import validators
from rest_framework import serializers
from drf_extra_fields import fields as extra_fields, relations as extra_relations
from .models import Banner, ProfilePicture, ContentImage


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            "id",
            "src_path",
            "src_url",
            "category",
            "is_active",
            "href",
            "alt",
            "src",
        ]
        extra_kwargs = {
            "src_path": {"write_only": True},
            "src_url": {"write_only": True},
        }


class ProfilePictureSerializer(serializers.ModelSerializer):
    image_data = extra_fields.Base64ImageField(
        write_only=True,
        required=False,
        source="src_path",
    )

    class Meta:
        model = ProfilePicture
        fields = [
            "id",
            "creation_user",
            "creation_date",
            "modification_date",
            "modification_user",
            "image_data",
            "src_path",
            "src_url",
            "is_user_property",
            "is_adult_only",
            "credits_url",
        ]
        read_only_fields = [
            "creation_user",
            "creation_date",
            "modification_date",
            "modification_user",
        ]
        extra_kwargs = {
            "src_path": {"read_only": True},
        }


class ContentImageSerializer(serializers.ModelSerializer):
    MAX_IMAGES = None
    MIN_DIMENSIONS = (None, None)  # largeur x hauteur
    MAX_DIMENSIONS = (None, None)  # largeur x hauteur
    WHITELIST = []

    image_data = extra_fields.Base64ImageField(
        write_only=True,
        required=False,
        source="src_path",
    )
    creation_user = extra_relations.PresentablePrimaryKeyRelatedField(
        presentation_serializer="users.serializers.UserCardSerializer",
        read_only=True,
    )
    modification_user = extra_relations.PresentablePrimaryKeyRelatedField(
        presentation_serializer="users.serializers.UserCardSerializer",
        read_only=True,
    )

    # FIXME - pour le branchement
    url = serializers.URLField(
        source="src_url",
        validators=[
            validators.URLValidator(
                schemes=["http", "https"],
                # TODO - whitelist
            )
        ]
    )

    class Meta:
        model = ContentImage
        fields = [
            "id",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "index",
            "image_data",
            "src_path",
            "src_url",
            "display_height",
            "display_width",
            "is_user_property",
            "is_adult_only",
            "is_visibility_coerced",
            "credits_url",
            "src",
            "href",
            "alt",
            "url",
        ]
        read_only_fields = [
            "creation_date",
            "modification_date",
            "src_path",
            "is_visibility_coerced",
        ]
        extra_kwargs = {
            "src_url": {
                "validators": [
                    validators.URLValidator(
                        schemes=["http", "https"],
                        # TODO - whitelist
                    )
                ]
            },
            # FIXME - pour le branchement
            "is_user_property": {
                "required": False,
                "default": True,
            },
            "is_adult_only": {
                "required": False,
            },
            "index": {
                "required": False,
            }
        }

    @classmethod
    def many_init(cls, *args, **kwargs):
        """
        Limite le nombre d'imbrications de ce désérialiseur.
        Ce nombre peut être défini dans les sous-classes
         ou bien être passé comme paramètre lors de l'instanciation.
        """

        kwargs.setdefault("max_length", cls.MAX_IMAGES)
        return super().many_init(*args, **kwargs)

    def __init__(self, instance=None, data=..., **kwargs):
        """
        Limite les dimensions de l'image de ce déserialiseur.
        Ces dimensions peuvent être définies dans les sous-classes
         ou bien être passées comme paramètres lors de l'instanciation.
        """

        self.whitelist = kwargs.pop("whitelist", self.WHITELIST)
        self.min_dimensions = kwargs.pop("min_dimensions", self.MIN_DIMENSIONS)
        self.max_dimensions = kwargs.pop("max_dimensions", self.MAX_DIMENSIONS)
        super().__init__(instance, data, **kwargs)

    def validate_url(self, attr):
        if self.whitelist:
            validators.URLValidator(
                schemes=["http", "https"],
                # TODO - whitelist regex ici
            )
        # TODO - potentiellement, sanitisation du lien ici ?
        return attr

    def validate(self, attrs):
        values = super().validate(attrs)
        
        min_width, min_height = self.min_dimensions
        max_width, max_height = self.max_dimensions

        min_dimensions = "{}x{}px".format(min_width or "?", min_height or "?")
        max_dimensions = "{}x{}px".format(max_width or "?", max_height or "?")

        message = "Les dimensions de l'image {} doivent être comprises entre {} et {}.".format(values["index"], min_dimensions, max_dimensions)

        if display_width := values.get("display_width", None):
            if min_width and min_width > display_width:
                raise serializers.ValidationError(message)
            if max_width and max_width < display_width:
                raise serializers.ValidationError(message)
        if display_height := values.get("display_height", None):
            if min_height and min_height > display_height:
                raise serializers.ValidationError(message)
            if max_height and max_height < display_height:
                raise serializers.ValidationError(message)

        return values
