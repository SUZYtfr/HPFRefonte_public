from rest_framework.serializers import *
from .models import Banner


class BannerSerializer(ModelSerializer):

    class Meta:
        model = Banner
        fields = "__all__"
