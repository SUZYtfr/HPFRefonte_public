from rest_framework.serializers import *
from .models import Banner, ProfilePicture


class BannerSerializer(ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"


class ProfilePictureSerializer(ModelSerializer):

    class Meta:
        model = ProfilePicture
        fields = "__all__"
