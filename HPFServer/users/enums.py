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


class ReviewPolicy(IntegerChoices):
    OFF = 0, "désactivé"
    WRITE_TEXT = 1, "écriture de review"
    SEE_TEXT = 2, "affichage de texte"  # + écriture
    WRITE_GRADING = 3, "notation de review"  # + écriture et visibilité
    SEE_GRADING = 4, "affichage de notation"  # + écriture et visibilité et notation


class ColorScheme(IntegerChoices):
    AUTO = 0, "Préférence système"
    LIGHT = 1, "Mode clair"
    DARK = 2, "Mode sombre"


class Sort(IntegerChoices):
    ALPHA_ASC = 0, "Ordre alphabétique"
    ALPHA_DESC = 1, "Ordre alphabétique inversé"
    MOST_RECENT = 2, "Ordre chronologique"
    MOST_RECENT_DESC = 3, "Ordre chronologique inversé"
