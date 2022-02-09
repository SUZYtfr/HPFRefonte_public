from .models import NewsArticle, NewsComment

from core.serializers import BaseModelSerializer


class NewsCommentSerializer(BaseModelSerializer):
    """Sérialiseur de commentaire d'actualité"""

    class Meta:
        model = NewsComment
        fields = "__all__"


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
