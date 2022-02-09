from rest_framework.serializers import *

from .models import User
from fictions.serializers import FictionCardSerializer
from django.utils import timezone


class UserCardSerializer(HyperlinkedModelSerializer):
    """Sérialiseur du lien vers une présentation d'utilisateur"""

    class Meta:
        model = User
        fields = (
            "id",
            "url",
            "nickname",
        )
        extra_kwargs = {
            "url": {"view_name": "users:user-detail",
                    "lookup_field": "pk"},
        }


class PublicUserSerializer(ModelSerializer):
    """Sérialiseur de présentation d'un utilisateur"""

    fictions = SerializerMethodField(method_name="_get_published_fictions")
    reviews_url = HyperlinkedIdentityField(
        view_name="reviews:user-reviews",
        lookup_field="pk",
        lookup_url_kwarg="pk",
    )
    last_login = StringRelatedField()
    user_links = StringRelatedField(many=True)

    creation_date = HiddenField(default=CreateOnlyDefault(default=timezone.now()))
    modification_date = HiddenField(default=timezone.now())

    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "realname",
            "email",
            "birthdate",
            "bio",
            "gender",
            "fictions",
            "last_login",
            "mean",
            "reviews_url",
            "creation_date",
            "modification_date",
            "user_links",
            "banner",
        )

    # # cf : https://stackoverflow.com/questions/28309507/django-rest-framework-filtering-for-serializer-field#28310334
    def _get_published_fictions(self, obj):
        """Renvoie la liste des fictions validées de l'auteur"""

        return FictionCardSerializer(obj.authored_fictions.filter(chapters__validation_status=7).distinct(),
                                     many=True,
                                     context=self.context).data
