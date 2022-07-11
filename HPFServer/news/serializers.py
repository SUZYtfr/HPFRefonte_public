from rest_framework.serializers import CreateOnlyDefault, ModelSerializer

from .models import NewsArticle, NewsComment

from users.models import User
from django.contrib.auth.models import Group

class NewsAuthorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
        ]


class NewsTeamSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]


class NewsSerializer(ModelSerializer):
    """Sérialiseur d'actualité"""

    authors = NewsAuthorSerializer(read_only=True, many=True)
    teams = NewsTeamSerializer(read_only=True, many=True)

    class Meta:
        model = NewsArticle
        fields = (
            "id",
            "title",
            "post_date",
            "category",
            "status",
            "content",
            "authors",
            "teams",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "comments",
        )
        read_only_fields = (
            "authors",
            "teams",
        )


class NewsCommentSerializer(ModelSerializer):
    """Sérialiseur de commentaire d'actualité"""

    class Meta:
        model = NewsComment
        fields = "__all__"
        read_only_fields = (
            "newsarticle",
        )
