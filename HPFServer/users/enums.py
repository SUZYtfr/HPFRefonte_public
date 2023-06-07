from django.db.models import IntegerChoices


class Gender(IntegerChoices):
    """Genres renseignés par les utilisateur·ice·s"""

    UNDEFINED = (0, "Non renseigné")
    FEMALE = (1, "Femme")
    MALE = (2, "Homme")
    OTHER = (3, "Autre")


class WebsiteType(IntegerChoices):
    """Sites web de profils d'utilisateur·ice·s"""

    FACEBOOK = (1, "Facebook")
    INSTAGRAM = (2, "Instagram")
    TWITTER = (3, "Twitter")
    YOUTUBE = (4, "Youtube")
    HPFANFICTION = (5, "HPFanfiction")
    LEHERON = (6, "Le Héron")
    FORUM = (7, "Forum HPF")
