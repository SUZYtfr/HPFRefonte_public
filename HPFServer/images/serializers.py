from rest_framework.serializers import *
from .models import Banner, ProfilePicture


class BannerSerializer(ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"


class ProfilePictureSerializer(ModelSerializer):
    class Meta:
        model = ProfilePicture
        fields = [
            "id",
            "creation_user",
            "creation_date",
            "modification_date",
            "modification_user",
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
