from rest_framework import serializers
from drf_extra_fields import fields as extra_fields
from .models import Banner, ProfilePicture


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"


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
            "src_link",
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
