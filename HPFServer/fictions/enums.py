from django.db.models import IntegerChoices, TextChoices


class FictionStatus(TextChoices):
    """Statuts d'écriture des fictions"""

    ONGOING = ("ONGOING", "En cours")
    PAUSED = ("PAUSED", "À l'arrêt")
    ABANDONED = ("ABANDONED", "Abandonnée")
    FINISHED = ("FINISHED", "Terminée")


class Rating(TextChoices):
    """Audience d'une fiction"""

    ALL = ("ALL", "Tout public")
    P12 = ("P12", "Déconseillé aux moins de 12 ans")
    P16 = ("P16", "Déconseillé aux moins de 16 ans")
    P18 = ("P18", "Déconseillé aux moins de 18 ans")


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


class CollectionAccess(TextChoices):
    """Niveaux d'accès aux séries"""

    CLOSED = ("CLOSED", "Fermée")
    MODERATED = ("MODERATED", "Modérée")
    OPEN = ("OPEN", "Ouverte")
