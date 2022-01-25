from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from core.models import DatedModel, CreatedModel


BANNER_MAX_SIZE = (468, 60)  # (largeur, hauteur)


def validate_maximum_size(image):
    error = False
    width, height = BANNER_MAX_SIZE
    if image.width > width:
        error = True
    if image.height > height:
        error = True
    if error:
        raise ValidationError(
            [f"La taille de la bannière doit être au maximum {width} x {height} pixels."]
        )


class Banner(DatedModel, CreatedModel):
    """Modèle de bannière"""

    class BannerType(models.IntegerChoices):
        WEBSITE = (1, "Bannière du site")
        PARTNER = (2, "Bannière de partenaire")
        EVENT = (3, "Bannière événementielle")
        PREMIUM = (4, "Bannière d'adhérent")

    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="banner", verbose_name="utilisateur", limit_choices_to={"is_premium": True})
    image = models.ImageField(upload_to="banners", validators=[validate_maximum_size])
    category = models.SmallIntegerField(choices=BannerType.choices)
    url = models.URLField(verbose_name="URL", null=True, blank=True)
    display_text = models.CharField(max_length=200, verbose_name="texte alternatif", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="active")

    class Meta:
        verbose_name = "bannière"

    def __str__(self):
        return self.image.url

    def delete(self, using=None, keep_parents=False):
        self.image.delete(save=False)
        super().delete(using, keep_parents)
