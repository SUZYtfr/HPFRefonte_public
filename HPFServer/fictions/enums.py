from django.db.models import IntegerChoices


class FictionStatus(IntegerChoices):
    """Statuts d'écriture des fictions"""

    PROGRESS = (1, "En cours")
    PAUSED = (2, "À l'arrêt")
    ABANDONED = (3, "Abandonnée")
    COMPLETED = (4, "Terminée")


class Rating(IntegerChoices):
    """Audience d'une fiction"""

    ALL = (1, "Tout public")
    P12 = (2, "Déconseillé aux moins de 12 ans")
    P16 = (3, "Déconseillé aux moins de 16 ans")
    P18 = (4, "Déconseillé aux moins de 18 ans")


class ChapterValidationStage(IntegerChoices):
    """Étapes de validation des chapitres"""

    DRAFT = (1, "Brouillon")
    BETA_ONGOING = (2, "Bêtatage en cours")
    BETA_COMPLETE = (3, "Bêtatage réalisé")
    PENDING = (4, "En cours de validation")
    EDIT_REQUIRED = (5, "En attente de modification")
    EDITED = (6, "Modifié")
    PUBLISHED = (7, "Publié")
    DISCUSSED = (8, "À discuter")


class CollectionAccess(IntegerChoices):
    """Niveaux d'accès aux séries"""

    CLOSED = (1, "Fermée")
    MODERATED = (2, "Modérée")
    OPEN = (3, "Ouverte")
