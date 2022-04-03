from rest_framework.serializers import CreateOnlyDefault, ModelSerializer

from .models import NewsArticle, NewsComment


class NewsSerializer(ModelSerializer):
    """Sérialiseur d'actualité"""

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
