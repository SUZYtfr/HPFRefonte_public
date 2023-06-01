from django.db.models import IntegerChoices


class BannerType(IntegerChoices):
    WEBSITE = (1, "Bannière du site")
    PARTNER = (2, "Bannière de partenaire")
    EVENT = (3, "Bannière événementielle")
    PREMIUM = (4, "Bannière d'adhérent")
    