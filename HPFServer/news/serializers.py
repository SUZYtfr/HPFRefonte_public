from django.db import transaction
from django.contrib.auth.models import Group
from rest_framework import serializers
from drf_extra_fields import relations as extra_relations

from core.serializers import ListableModelSerializer
from .models import NewsArticle, NewsComment

from images.models import ContentImage
from images.serializers import ContentImageSerializer


class NewsCommentSerializer(serializers.ModelSerializer):
    """Sérialiseur de commentaire d'actualité"""

    # FIXME - pour le branchement
    content = serializers.CharField(
        source="text",
    )
    content_images = ContentImageSerializer(
        many=True,
        max_length=1,
        required=False,
        source="text_images",
    )
    post_date = serializers.DateTimeField(
        source="creation_date",
        read_only=True,
    )
    author = extra_relations.PresentablePrimaryKeyRelatedField(
        source="creation_user",
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )

    class Meta:
        model = NewsComment
        fields = [
            "id",
            "content",
            "author",
            "post_date",
            "creation_date",
            "creation_user",
            "modification_date",
            "modification_user",
            "content_images",
        ]

    @transaction.atomic
    def create(self, validated_data):        
        text_images = validated_data.pop("text_images", None)
        news_comment = super().create(validated_data=validated_data)

        if text_images:
            images = [
                ContentImage(
                    **_hpf_image,
                    creation_user=validated_data["creation_user"],                
                ) for _hpf_image in text_images
            ]
            images = ContentImage.objects.bulk_create(images)
            news_comment.text_images.set(images)
    
        return news_comment


class NewsTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            "id",
            "name",
        ]


class NewsArticleListSerializer(serializers.ModelSerializer):
    authors = extra_relations.PresentablePrimaryKeyRelatedField(
        many=True,
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    teams = NewsTeamSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = NewsArticle
        fields = [
            "id",
            "title",
            "post_date",
            "category",
            "status",
            "content",
            "authors",
            "teams",
            "comment_count",
        ]


class NewsArticleSerializer(ListableModelSerializer):
    """Sérialiseur d'actualité"""

    authors = extra_relations.PresentablePrimaryKeyRelatedField(
        many=True,
        read_only=True,
        presentation_serializer="users.serializers.UserCardSerializer",
    )
    teams = NewsTeamSerializer(read_only=True, many=True)
    comments = NewsCommentSerializer(read_only=True, many=True)

    content_images = ContentImageSerializer(many=True)

    class Meta:
        list_serializer_child_class = NewsArticleListSerializer
        model = NewsArticle
        fields = [
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
            "comment_count",
            "content_images",
        ]

    @transaction.atomic
    def create(self, validated_data):        
        content_images = validated_data.pop("content_images", None)
        newsarticle = super().create(validated_data=validated_data)

        if content_images:
            images = [
                ContentImage(
                    **_hpf_image,
                    creation_user=validated_data["creation_user"],                
                ) for _hpf_image in content_images
            ]
            images = ContentImage.objects.bulk_create(images)
            newsarticle.content_images.set(images)
    
        return newsarticle
