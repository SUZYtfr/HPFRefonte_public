from rest_framework.serializers import *

from .models import User
from fictions.serializers import FictionCardSerializer


# TODO
class UserStats(ModelSerializer):
    pass


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


class UserSerializer(ModelSerializer):
    """Sérialiseur d'utilisateur"""

    fictions = SerializerMethodField(method_name="_get_fictions", read_only=True)
    reviews_url = HyperlinkedIdentityField(
        view_name="reviews:users:object-review-list",
        lookup_field="pk",
        lookup_url_kwarg="object_pk",
        read_only=True,
    )
    user_links = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "realname",
            "email",
            "birthdate",
            "bio",
            "gender",
            "age_consent",
            "fictions",
            "last_login",
            "mean",
            "reviews_url",
            "creation_date",
            "modification_date",
            "user_links",
            "banner",
        ]
        read_only_fields = [
            "banner",
        ]
        extra_kwargs = {
            "gender": {"write_only": True},
            "age_consent": {"write_only": True},
            "email": {"write_only": True},
            "birthdate": {"write_only": True},
            "realname": {"write_only": True},
        }

    def _get_fictions(self, obj):
        """Renvoie la liste des fictions validées de l'auteur"""

        return FictionCardSerializer(obj.authored_fictions.filter(chapters__validation_status=7).distinct(),
                                     many=True,
                                     context=self.context).data
