import os.path
from django.db import models
from django.conf import settings
from core.models import CreatedModel, DatedModel

from .enums import BannerType


"""
Toutes les images sont répertoriées dans la BDD. Aucune image ne doit être insérée par une balise <img>.
En plus des métadonnées habituelles (de création et modification), les informations d'images sont enregistrées
dans autant de tables que de types d'images.
Une image peut être hébergée intérieurement ou extérieurement, selon des droits à établir.
"""


def upload_function(instance, filename):
    dirname = instance.upload_folder
    return instance.src_path.field.storage.generate_filename(os.path.join(dirname, filename))


class BaseImage(CreatedModel, DatedModel):
    """Modèle de base pour les images
    
    
    :src_url est l'URL de l'image si hébergée extérieurement
    :src_path est le chemin d'accès de l'image si hébergée intérieurement
    :src renvoie l'URL dans le premier cas absolu, dans le second relatif, de l'image

    Concernant les images hébergées intérieurement :
    :upload_folder est le dossier de MEDIA_ROOT (et MEDIA_URL) dans lequel l'image d'un type est accessible

    Un UUID est automatiquement formé pour le nom de l'image.

    :display_height et
    :display_width sont les dimensions de l'image déclarées
    Qu'il s'agisse d'une image interne, que l'on contrôle, ou externe, que l'on ne contrôle pas,
    ce sont les dimensions selon lesquelles l'image devrait apparaître dans le contenu, si applicable.
"""

    upload_folder = "images"

    # Origine de l'image
    src_path = models.ImageField(
        upload_to=upload_function,
        null=True,
        blank=True,
        verbose_name="chemin de l'image",
        help_text="Chemin vers l'image si herbergée intérieurement."
    )
    src_url = models.URLField(
        null=True,
        blank=True,
        verbose_name="URL de l'image",
        help_text="URL vers l'image si hébergée extérieurement."
    )

    # Apparence et comportement de l'image
    display_height = models.PositiveSmallIntegerField()
    display_width = models.PositiveSmallIntegerField()
    href = models.URLField(
        null=True,
        blank=True,
        verbose_name="URL de la balise",
        help_text="URL de la balise de lien de l'image si applicable."    
    )
    alt = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="texte alternatif",
        help_text="Text alternatif de l'image si applicable."
    )

    class Meta:
        abstract = True
        verbose_name = "image"

    @property
    def src(self) -> str:
        """URL source interne relative ou externe absolue de l'image"""

        if self.src_path:
            return self.src_path.url
        elif self.src_url:
            return self.src_url
        else:
            return ""

    def delete(self, *args, **kwargs):
        """En cas de suppression de la ressource, s'assure que toute image hébergée intérieurement est également supprimée"""

        self.src_path.delete(save=False)
        super().delete(*args, **kwargs)

    @property
    def is_on_disk(self) -> bool:
        """Indique si l'image est hébergée intérieurement"""

        return bool(self.src_path)

    def __str__(self):
        filename = self.src.split("/")[-1]
        on_disk = " (sur disque)" if self.is_on_disk else ""
        return f"{filename}{on_disk}"


class Banner(BaseImage):
    """Modèle de bannière"""

    upload_folder = "banners"

    user_profile = models.OneToOneField(
        verbose_name="profil",
        to="users.UserProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_banner",
        editable=True,
    )
    category = models.IntegerField(
        choices=BannerType.choices,
        verbose_name="catégorie",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="bannière active",
        help_text="Indique si la bannière doit être affichée",
    )

    class Meta:
        verbose_name = "bannière"

    def __str__(self):
        owner = " de {}".format(self.user_profile.user.username) if self.user_profile else ""
        status = "active" if self.is_active else "inactive"
        on_disk = " (sur disque)" if self.is_on_disk else ""
        return f"Bannière{owner} {status}{on_disk}"

"""
Ce modèle était pensé pour mettre une image en exergue pour les news, un peu comme sur WP
Mais du moins pour commencer, utiliser plutôt ContentImage
"""
# class NewsPicture(BaseImage):
#     """Modèle d'image de news"""

#     upload_folder = "newspictures"

#     newsarticle = models.ForeignKey(
#         to="news.NewsArticle",
#         on_delete=models.CASCADE,
#         editable=True,
#         verbose_name="news",
#     )

#     class Meta:
#         verbose_name = "image de news"
#         verbose_name_plural = "images de news"


class BaseUserImage(BaseImage):
    """
    Modèle de base d'image ajoutée par les utilisateurs
    
    :is_adult_only indique si l'image a un public restreint
    :is_visibility_coerced indique si seule la modération peut modifier la valeur précédente
    """
    
    is_user_property = models.BooleanField(
        verbose_name="propriété de l'utilisateur",
        help_text="Indique si l'utilisateur a spécifiquement indiqué que l'image lui appartient ou que les droits lui ont été cédés."
    )
    credits_url = models.URLField(
        null=True,
        blank=True,
        verbose_name="URL du site",
        help_text="URL du site du propriétaire de l'image si applicable."
    )
    is_adult_only = models.BooleanField(
        verbose_name="public restreint",
    )
    is_visibility_coerced = models.BooleanField(
        default=False,
        verbose_name="imposé par la modération",
    )

    class Meta:
        abstract = True
        verbose_name = "image d'utilisateur"
        verbose_name_plural = "images d'utilisateurs"


class ProfilePicture(BaseUserImage):
    """Modèle d'image de profil d'utilisateur"""

    upload_folder = "profilepictures"

    user_profile = models.OneToOneField(
        to="users.UserProfile",
        on_delete=models.CASCADE,
        verbose_name="image de profil",
        related_name="user_profile_picture",
        editable=True,
    )

    class Meta:
        verbose_name = "image de profil"
        verbose_name_plural = "images de profils"


class ContentImage(BaseUserImage):
    """
    Modèle d'image de contenu
    
    Ces images sont intégrées dans un corps de texte et doivent être liées
    à la ressource contenant ce texte par un M2M :
    Chapter.text_images = M2M -> ContentImage
    Chapter.start_note_images = M2M -> ContentImage

    Dans le corps du texte, une balise symbolise un ContentImage :
    Chapter.text = "Deux images <hpf_img index=1> <hpf_img index=2> intégrées dans le corps de texte"
    """

    upload_folder = "contentimages"

    index = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "image de contenu"
        verbose_name_plural = "images de contenu"

    def __str__(self):
        return "Image de contenu {}".format("interne" if self.is_on_disk else "externe")
