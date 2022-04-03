from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from core.models import CreatedModel, DatedModel
import os.path


def upload_function(instance, filename):
    dirname = instance.upload_folder
    return instance.src_path.field.storage.generate_filename(os.path.join(dirname, filename))


class BaseImage(CreatedModel, DatedModel):
    """Modèle de base pour les images"""

    upload_folder = "images"

    src_path = models.ImageField(upload_to=upload_function,
                                 null=True, blank=True,
                                 verbose_name="chemin de l'image")  # interne
    src_link = models.URLField(null=True, blank=True,
                               verbose_name="URL de l'image")  # externe

    class Meta:
        abstract = True
        verbose_name = "image"

    @property
    def src_url(self):
        """Renvoie l'URL source interne relative ou externe absolue de l'image"""

        if self.src_path:
            return self.src_path.url
        elif self.src_link:
            return self.src_link
        else:
            return ""
        # return self.src_path.url or self.src_link or ""

    def delete(self, using=None, keep_parents=False):
        """En cas de suppression de la ressource, s'assure que toute image hébergée est également supprimée"""

        self.src_path.delete(save=False)
        super().delete(using, keep_parents)

    def clean(self):
        if not (self.src_link or self.src_path):
            raise ValidationError("Un lien doit être indiqué ou une image téléversée.")
        if self.src_link and self.src_path:
            raise ValidationError("Une image ne peut être téléversée si un lien est indiqué.")

    @property
    def is_uploaded(self):
        return bool(self.src_path)

    def __str__(self):
        filename = self.src_url.split("/")[-1]
        on_disk = " (sur disque)" if self.is_uploaded else ""
        return f"{filename}{on_disk}"


class Banner(BaseImage):
    """Modèle de bannière"""

    upload_folder = "banners"

    class BannerType(models.IntegerChoices):
        WEBSITE = (1, "Bannière du site")
        PARTNER = (2, "Bannière de partenaire")
        EVENT = (3, "Bannière événementielle")
        PREMIUM = (4, "Bannière d'adhérent")

    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=True, blank=True, editable=False,
                                verbose_name="utilisateur")
    category = models.SmallIntegerField(choices=BannerType.choices,
                                        verbose_name="catégorie")
    is_active = models.BooleanField(default=True,
                                    verbose_name="bannière active")

    href = models.URLField(null=True, blank=True,
                           verbose_name="URL du lien")
    display_text = models.CharField(max_length=200, null=True, blank=True,
                                    verbose_name="texte alternatif")

    class Meta:
        verbose_name = "bannière"

    def __str__(self):
        owner = " de {}".format(self.user.nickname) if self.user else ""
        status = "active" if self.is_active else "inactive"
        on_disk = " (sur disque)" if self.is_uploaded else ""
        return f"Bannière{owner} {status}{on_disk}"


class NewsPicture(BaseImage):
    """Modèle d'image de news"""

    upload_folder = "newsimages"

    newsarticle = models.ForeignKey(to="news.NewsArticle", on_delete=models.CASCADE,
                                    verbose_name="news")

    class Meta:
        verbose_name = "image de news"
        verbose_name_plural = "images de news"


class BaseUserImage(BaseImage):
    """Modèle de base d'image ajoutée par les utilisateurs"""

    is_user_property = models.BooleanField(verbose_name="propriété de l'utilisateur")
    is_adult_only = models.BooleanField(verbose_name="tout public")
    credits_url = models.URLField(null=True, blank=True,
                                  verbose_name="URL du site du propriétaire")

    def clean(self):
        super(BaseUserImage, self).clean()

        if not (self.is_user_property or self.credits_url):
            raise ValidationError("Un lien vers le site web crédité est requis si l'image n'appartient pas à l'utilisateur.")

    class Meta:
        abstract = True
        verbose_name = "image d'utilisateur'"
        verbose_name_plural = "images d'utilisateurs'"


class ProfilePicture(BaseUserImage):
    """Modèle d'image de profil d'utilisateur"""

    upload_folder = "profilepictures"

    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                verbose_name="utilisateur")

    class Meta:
        verbose_name = "image de profil"
        verbose_name_plural = "images de profils"


class ContentPicture(BaseUserImage):
    """Modèle d'image de contenu"""

    pass
    # TODO - lier l'image à son contenu: FK(to=Chapter) + FK(to=Fiction)... ou GFK?

    class Meta:
        verbose_name = "image de contenu"
        verbose_name_plural = "images de contenu"
