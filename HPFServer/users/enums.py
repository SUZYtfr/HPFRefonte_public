from django.db.models import IntegerChoices

class Gender(IntegerChoices):
    """Genres renseignés par les utilisateur·ice·s"""

    UNDEFINED = (0, "Non renseigné")
    FEMALE = (1, "Femme")
    MALE = (2, "Homme")
    OTHER = (3, "Autre")
