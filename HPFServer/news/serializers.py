from rest_framework.serializers import ModelSerializer
from drf_extra_fields import relations as extra_relations

from .models import NewsArticle, NewsComment

from django.contrib.auth.models import Group


class NewsTeamSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]


class NewsSerializer(ModelSerializer):
    """Sérialiseur d'actualité"""

    authors = extra_relations.PresentablePrimaryKeyRelatedField(
        many=True,
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
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
