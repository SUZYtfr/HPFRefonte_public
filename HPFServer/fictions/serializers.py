from rest_framework.serializers import *
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from users.models import User

from .models import Fiction, Chapter, Beta
from features.models import Category, Feature

from core.text_functions import read_text_file


# ALLOWED_EXTENSIONS = ["txt", "doc", "docx", "odt"]
ALLOWED_EXTENSIONS = ["txt", "docx"]


class FeaturesChoiceRelatedField(RelatedField):
    """Champ de choix de caractéristiques"""

    queryset = Feature.allowed.all()

    def to_representation(self, value):
        """Renvoie l'ID de la caractéristique pour sérialisation"""

        return value.pk

    def get_choices(self, cutoff=None):
        """Renvoie les caractéristiques groupées par catégories"""

        return {
            category.name:
                {feature.pk: feature.name for feature in category.features.all()}
            for category in Category.objects.all()
        }

    def to_internal_value(self, data):
        """Renvoie la caractéristique correspondant à l'ID pour désérialisation"""

        try:
            feature = self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            raise ValidationError("La caractéristique avec l'ID {} n'a pas été trouvée.".format(data))

        return feature


class FictionSerializer(ModelSerializer):
    """Sérialiseur privé de fiction"""

    read_count = IntegerField(read_only=True)
    word_count = IntegerField(read_only=True)

    class Meta:
        model = Fiction
        fields = "__all__"
        read_only_fields = (
            "authors",
            "word_count",
            "mean",
            "status",
            "read_count",
            "chapters",
        )
        extra_kwargs = {
            "featured": {"read_only": True}
        }

    features = FeaturesChoiceRelatedField(
        many=True,
    )

    reviews_url = HyperlinkedIdentityField(
        view_name="reviews:fictions:object-review-list",
        lookup_field="pk",
        lookup_url_kwarg="object_pk",
    )

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
            raise ValidationError(" ".join([below, above]))

        return value


class FictionCardSerializer(FictionSerializer):
    """Sérialiseur de carte de fiction"""

    class Meta(FictionSerializer.Meta):
        fields = (
            "id",
            "title",
        )


class FictionExtraAuthorSerializer(Serializer):
    """Sérialiseur d'ajout d'auteur à une fiction"""

    class AuthorNicknameField(CharField):
        def to_internal_value(self, data):
            try:
                user = User.objects.get(nickname=data)
            except User.DoesNotExist:
                raise ValidationError(f"L'utilisateur {data} n'a pas été trouvé.")

            return user

    author_nickname = AuthorNicknameField(write_only=True)
    authors = StringRelatedField(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.authors.add(validated_data["author_nickname"])
        return instance


class ChapterSerializer(ModelSerializer):
    """Sérialiseur de chapitre"""

    order = SerializerMethodField()

    reviews_url = HyperlinkedIdentityField(
        view_name="reviews:chapters:object-review-list",
        lookup_field="pk",
        lookup_url_kwarg="object_pk",
    )

    text_file_upload = FileField(allow_null=True, allow_empty_file=True, write_only=True, validators=[
        FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS,
                               message="L'extension de fichier %(extension)s n'est pas pris en charge. "
                                       "Les extensions de fichiers autorisés sont %(allowed_extensions)s.")
    ])

    text = CharField(allow_blank=True, style={'base_template': 'textarea.html'})

    class Meta:
        model = Chapter
        fields = "__all__"
        read_only_fields = (
            "order",
            "validation_status",
            "word_count",
            "read_count",
            "mean",
            "poll",
            "reviews_url",
            "fiction",
        )

    def validate_text_file_upload(self, value):
        if value:
            try:
                return read_text_file(value)
            except Exception as e:
                raise ValidationError(e)

    def validate(self, attrs):
        if not attrs.get("text"):
            if not attrs.get("text_file_upload"):
                raise ValidationError("Le texte du chapitre doit être passé.")
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
        fields = (
            "id",
            "title",
            "order",
        )


class FictionChapterOrderSerializer(ModelSerializer):

    class Meta:
        model = Fiction
        fields = ("order",)

    order = ListField(
        child=IntegerField(),
        source="get_chapter_order",
    )

    def validate_order(self, value):

        if not len(set(value)) == len(value):
            raise ValidationError("Des ID de chapitres sont en double.")

        if not set(self.instance.get_chapter_order()) == set(value):
            raise ValidationError("Les ID de chapitres passés ne correspondent pas aux ID existants.")

        return value

    def reorder(self):
        self.instance.set_chapter_order(self.validated_data["get_chapter_order"])


class BetaSerializer(ModelSerializer):
    """Sérialiseur de bêtatage"""

    class ChapterField(PrimaryKeyRelatedField):
        """Champ de choix de chapitres pour le bêtatage"""

        def get_queryset(self):
            """Renvoie la liste des chapitres à l'état de brouillon de l'utilisateur authentifié

                Exclut les chapitres avec un bêtatage en cours."""

            queryset = Chapter.objects.filter(
                authors=self.context["request"].user,
                validation_status__in=[
                    Chapter.ChapterValidationStage.DRAFT,
                    Chapter.ChapterValidationStage.BETA_COMPLETE,
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


class BetaActionSerializer(ModelSerializer):
    """Sérialiseur d'actions de bêtatage"""

    def __init__(self, *args, **kwargs):
        """Redéfinition de l'initialisation du sérialiseur

            Afin de pouvoir proposer des choix d'actions dynamiques par rapport au bêtatage en cours,
            on laisse le sérialiseur s'initialiser normalement, puis une fois l'instance passée, on modifie
            les choix (et la valeur initiale) selon cette instance."""

        super(ModelSerializer, self).__init__(*args, **kwargs)
        if self.instance:
            corres = STAGE_TO_CHOICES_AND_INITIAL_DICT.get(self.instance.stage, None)
            if corres:
                self.fields["stage"].choices = corres.get("choices")
                self.fields["stage"].initial = corres.get("initial")
            if self.instance.stage == Beta.BetaStage.REQUESTED:
                self.fields["text"].read_only = True

    class TextField(CharField):
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
                instance.chapter.validation_status = Chapter.ChapterValidationStage.BETA_ONGOING
                instance.chapter.modification_user = self.context["request"].user
        elif stage == Beta.BetaStage.CORRECTED:
            instance.chapter.create_text_version(creation_user=self.context["request"].user, text=text)
            instance.chapter.modification_user = self.context["request"].user
        elif stage == Beta.BetaStage.COMPLETED:
            instance.chapter.validation_status = Chapter.ChapterValidationStage.BETA_COMPLETE
            instance.chapter.modification_user = self.context["request"].user
        instance.chapter.save()

        return super().update(instance, validated_data)