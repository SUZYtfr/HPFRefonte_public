from .models import NewsArticle, NewsComment

from core.serializers import BaseModelSerializer


class NewsCommentSerializer(BaseModelSerializer):
    """Sérialiseur de commentaire d'actualité"""

    class Meta:
        model = NewsComment
        exclude = (
            "modification_date",
            "modification_user",
            "newsarticle",
        )


class NewsSerializer(BaseModelSerializer):
    """Sérialiseur d'actualité"""

    comments = NewsCommentSerializer(many=True)

    class Meta:
        model = NewsArticle
        fields = (
            "id",
            "post_date",
            "title",
            "content",
            "category",
            "authors",
            "teams",
            "comments",
        )