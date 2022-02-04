from rest_framework.serializers import *
from .models import Banner, ProfilePicture
from core.serializers import BaseModelSerializer


class BannerSerializer(BaseModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"


class ProfilePictureSerializer(BaseModelSerializer):

    class Meta:
        model = ProfilePicture
        fields = "__all__"
