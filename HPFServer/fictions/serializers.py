from rest_framework import serializers, exceptions
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from users.models import User

from .models import Fiction, Chapter, Beta
from features.models import Category, Feature
from features.serializers import FeatureCardSerializer
from users.serializers import UserCardSerializer
from colls.models import Collection
from core.serializers import ListableModelSerializer, CardSerializer
from core.text_functions import read_text_file
from reviews.models import Review

# ALLOWED_EXTENSIONS = ["txt", "doc", "docx", "odt"]
ALLOWED_EXTENSIONS = ["txt", "docx"]


# class serializers.FeaturesChoiceRelatedField(serializers.RelatedField):
#     """Champ de choix de caractéristiques"""
#
#     queryset = Feature.allowed.all()
#
#     def to_representation(self, value):
#         """Renvoie l'ID de la caractéristique pour sérialisation"""
#
#         return value.pk
#
#     def get_choices(self, cutoff=None):
#         """Renvoie les caractéristiques groupées par catégories"""
#
#         return {
#             category.name:
#                 {feature.pk: feature.name for feature in category.features.all()}
#             for category in Category.objects.all()
#         }
#
#     def to_internal_value(self, data):
#         """Renvoie la caractéristique correspondant à l'ID pour désérialisation"""
#
#         try:
#             feature = self.get_queryset().get(pk=data)
#         except ObjectDoesNotExist:
#             raise ValidationError("La caractéristique avec l'ID {} n'a pas été trouvée.".format(data))
#
#         return feature

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "title",
        ]


class FictionListSerializer(serializers.ModelSerializer):
    features = FeatureCardSerializer(many=True)
    creation_user = CardSerializer(read_only=True)
    authors = serializers.SerializerMethodField()
    series = CollectionSerializer(read_only=True, many=True, source="collections")

    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
            "creation_user",
            "creation_date",
            "last_update_date",
            "mean",
            "summary",
            "storynote",
            "status",
            "read_count",
            "word_count",
            "collection_count",
            "featured",
            "features",
            "authors",
            "series",
            "chapter_count",
            "review_count",
        ]

    def get_authors(self, obj):
        author = obj.creation_user
        return [UserCardSerializer(instance=author).data]


class FictionSerializer(ListableModelSerializer):
    """Sérialiseur privé de fiction"""

    features = FeatureCardSerializer(many=True)
    creation_user = CardSerializer(read_only=True)
    authors = serializers.SerializerMethodField()
    series = CardSerializer(read_only=True, many=True, source="collections")
    member_review_policy = serializers.IntegerField(read_only=True, source="creation_user.preferences.member_review_policy")
    anonymous_review_policy = serializers.IntegerField(read_only=True, source="creation_user.preferences.anonymous_review_policy")

    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "coauthors",
            "last_update_date",
            "mean",
            "summary",
            "storynote",
            "status",
            "read_count",
            "word_count",
            "collection_count",
            "featured",
            "features",
            "authors",
            "series",
            "chapter_count",
            "review_count",
            "member_review_policy",
            "anonymous_review_policy",
        ]
        read_only_fields = (
            "coauthors",
            "word_count",
            "mean",
            "status",
            "read_count",
            "chapters",
            "featured",
        )
        list_serializer_child_class = FictionListSerializer

    def get_authors(self, obj):
        author = obj.creation_user
        return [UserCardSerializer(instance=author).data]

    # def get_series(self, obj):
    #     collections = Collection.objects.filter(
    #         chapters__fiction=obj,
    #         chapters__validation_status=Chapter.ValidationStage.PUBLISHED,
    #     ).distinct()
    #     return CollectionSerializer(collections, many=True).data


    # features = serializers.FeaturesChoiceRelatedField(
    #     many=True,
    # )

    # reviews_url = serializers.HyperlinkedIdentityField(
    #     view_name="reviews:fictions:object-review-list",
    #     lookup_field="pk",
    #     lookup_url_kwarg="object_pk",
    # )

    def validate_features(self, value):
        """Valide le nombre de caractéristiques pour chaque catégorie"""

        category_count = []

        for feature in value:
            category_count.append(feature.category.id)

        result = {"below_minimum": [], "above_maximum": []}
        for category in Category.objects.all():
            cat_id_count = category_count.count(category.id)
            if cat_id_count < category.min_limit:
                result["below_minimum"].append(str(category.min_limit - cat_id_count) + " " + category.name)
            if cat_id_count > (category.max_limit or float("inf")):
                result["above_maximum"].append(str(cat_id_count - category.max_limit) + " " + category.name)

        below = ""
        above = ""

        if result["below_minimum"]:
            below = f"Sélectionner {', '.join(result['below_minimum'])} en plus."
        if result["above_maximum"]:
            above = f"Sélectionner {', '.join(result['above_maximum'])} en moins."

        if below or above:
            raise exceptions.ValidationError(" ".join([below, above]))

        return value


class FictionCardSerializer(serializers.ModelSerializer):
    """Sérialiseur de carte de fiction"""

    class Meta:
        model = Fiction
        fields = [
            "id",
            "title",
        ]


class FictionExtraAuthorSerializer(serializers.Serializer):
    """Sérialiseur d'ajout d'auteur à une fiction"""

    class AuthorNicknameField(serializers.CharField):
        def to_internal_value(self, data):
            try:
                user = User.objects.get(nickname=data)
            except User.DoesNotExist:
                raise exceptions.ValidationError(f"L'utilisateur {data} n'a pas été trouvé.")

            return user

    author_nickname = AuthorNicknameField(write_only=True)
    authors = serializers.StringRelatedField(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.authors.add(validated_data["author_nickname"])
        return instance


class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
        ]


class ChapterSerializer(ListableModelSerializer):
    """Sérialiseur de chapitre"""

    order = serializers.SerializerMethodField()
    # mean = serializers.IntegerField(default=None)

    # text_file_upload = serializers.FileField(allow_null=True, allow_empty_file=True, write_only=True, validators=[
    #     FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS,
    #                            message="L'extension de fichier %(extension)s n'est pas pris en charge. "
    #                                    "Les extensions de fichiers autorisés sont %(allowed_extensions)s.")
    # ])

    # text = serializers.CharField(allow_blank=True, style={'base_template': 'textarea.html'})

    member_review_policy = serializers.IntegerField(
        read_only=True,
        source="fiction.creation_user.preferences.member_review_policy",
    )
    anonymous_review_policy = serializers.IntegerField(
        read_only=True,
        source="fiction.creation_user.preferences.anonymous_review_policy",
    )

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "fiction",
            "creation_user",
            "creation_date",
            "modification_user",
            "modification_date",
            "startnote",
            "endnote",
            "order",
            "validation_status",
            "word_count",
            "read_count",
            "review_count",
            "mean",
            "poll",
            # "reviews_url",
            "member_review_policy",
            "anonymous_review_policy",
        ]
        read_only_fields = (
            "order",
            "validation_status",
            "word_count",
            "read_count",
            "mean",
            "poll",
            # "reviews_url",
            "fiction",
        )
        list_serializer_child_class = ChapterListSerializer

    def validate_text_file_upload(self, value):
        if value:
            try:
                return read_text_file(value)
            except Exception as e:
                raise exceptions.ValidationError(e)

    def validate(self, attrs):
        if not attrs.get("text"):
            if not attrs.get("text_file_upload"):
                raise exceptions.ValidationError("Le texte du chapitre doit être passé.")
            attrs.update({"text": attrs.get("text_file_upload")})
        attrs.pop("text_file_upload")
        return attrs

    def create(self, validated_data):
        text = validated_data.pop("text")
        instance = super().create(validated_data)
        instance.create_text_version(
            text=text,
            creation_user=self.context["request"].user,
            touch=False,
        )
        return instance

    def update(self, instance, validated_data):
        text = validated_data.pop("text")
        instance = super().update(instance, validated_data)
        instance.create_text_version(
            text=text,
            creation_user=self.context["request"].user,
            touch=True
        )
        return instance

    def get_order(self, obj):
        return obj._order + 1  # index 0 -> 1


class ChapterCardSerializer(ChapterSerializer):
    """Sérialiseur de carte de chapitre"""

    class Meta(ChapterSerializer.Meta):
        fields = [
            "id",
            "title",
            "order",
        ]


class FictionChapterOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fiction
        fields = ("order",)

    order = serializers.ListField(
        child=serializers.IntegerField(),
        source="get_chapter_order",
    )

    def validate_order(self, value):

        if not len(set(value)) == len(value):
            raise exceptions.ValidationError("Des ID de chapitres sont en double.")

        if not set(self.instance.get_chapter_order()) == set(value):
            raise exceptions.ValidationError("Les ID de chapitres passés ne correspondent pas aux ID existants.")

        return value

    def reorder(self):
        self.instance.set_chapter_order(self.validated_data["get_chapter_order"])


class BetaSerializer(serializers.ModelSerializer):
    """Sérialiseur de bêtatage"""

    class ChapterField(serializers.PrimaryKeyRelatedField):
        """Champ de choix de chapitres pour le bêtatage"""

        def get_queryset(self):
            """Renvoie la liste des chapitres à l'état de brouillon de l'utilisateur authentifié

                Exclut les chapitres avec un bêtatage en cours."""

            queryset = Chapter.objects.filter(
                authors=self.context["request"].user,
                validation_status__in=[
                    Chapter.ValidationStage.DRAFT,
                    Chapter.ValidationStage.BETA_COMPLETE,
                ]
            ).exclude(
                beta__stage__in=[
                    Beta.BetaStage.REQUESTED,
                    Beta.BetaStage.ONGOING,
                    Beta.BetaStage.CORRECTED,
                ]
            )
            return queryset

    chapter = ChapterField()

    class Meta:
        model = Beta
        fields = ("chapter", "user", "stage", "text",)
        read_only_fields = ("stage", "text",)


STAGE_TO_CHOICES_AND_INITIAL_DICT = {
    Beta.BetaStage.REQUESTED.value: {
        "choices": [
            (Beta.BetaStage.ONGOING, "Accepter"),
            (Beta.BetaStage.REFUSED, "Refuser"),
        ],
        "initial": Beta.BetaStage.ONGOING,
    },
    Beta.BetaStage.ONGOING.value: {
        "choices": [
            (Beta.BetaStage.ONGOING, "Continuer"),
            (Beta.BetaStage.CORRECTED, "Proposer"),
        ],
        "initial": Beta.BetaStage.CORRECTED,
    },
    Beta.BetaStage.CORRECTED.value: {
        "choices": [
            (Beta.BetaStage.CORRECTED, "Continuer"),
            (Beta.BetaStage.ONGOING, "Renvoyer"),
            (Beta.BetaStage.COMPLETED, "Compléter"),
        ],
        "initial": Beta.BetaStage.COMPLETED,
    },
}


class BetaActionSerializer(serializers.ModelSerializer):
    """Sérialiseur d'actions de bêtatage"""

    def __init__(self, *args, **kwargs):
        """Redéfinition de l'initialisation du sérialiseur

            Afin de pouvoir proposer des choix d'actions dynamiques par rapport au bêtatage en cours,
            on laisse le sérialiseur s'initialiser normalement, puis une fois l'instance passée, on modifie
            les choix (et la valeur initiale) selon cette instance."""

        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)
        if self.instance:
            corres = STAGE_TO_CHOICES_AND_INITIAL_DICT.get(self.instance.stage, None)
            if corres:
                self.fields["stage"].choices = corres.get("choices")
                self.fields["stage"].initial = corres.get("initial")
            if self.instance.stage == Beta.BetaStage.REQUESTED:
                self.fields["text"].read_only = True

    class TextField(serializers.CharField):
        def to_internal_value(self, data):
            return data

    text = TextField()

    class Meta:
        model = Beta
        fields = ("chapter", "user", "stage", "text",)
        read_only_fields = ("chapter", "user",)

    def update(self, instance, validated_data):

        stage = validated_data.get("stage")
        text = validated_data.pop("text", None)

        if stage == Beta.BetaStage.ONGOING:
            if text:
                instance.chapter.create_text_version(creation_user=self.context["request"].user, text=text)
            else:
                instance.chapter.validation_status = Chapter.ValidationStage.BETA_ONGOING
                instance.chapter.modification_user = self.context["request"].user
        elif stage == Beta.BetaStage.CORRECTED:
            instance.chapter.create_text_version(creation_user=self.context["request"].user, text=text)
            instance.chapter.modification_user = self.context["request"].user
        elif stage == Beta.BetaStage.COMPLETED:
            instance.chapter.validation_status = Chapter.ValidationStage.BETA_COMPLETE
            instance.chapter.modification_user = self.context["request"].user
        instance.chapter.save()

        return super().update(instance, validated_data)
