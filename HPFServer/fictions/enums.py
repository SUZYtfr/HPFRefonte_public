from django.db.models import IntegerChoices


class FictionStatus(IntegerChoices):
    """Statuts d'écriture des fictions"""

    PROGRESS = (1, "En cours")
    PAUSED = (2, "À l'arrêt")
    ABANDONED = (3, "Abandonnée")
    COMPLETED = (4, "Terminée")


class ChapterValidationStage(IntegerChoices):
    """Étapes de validation des chapitres"""

    DRAFT = (1, "Brouillon")
    BETA_ONGOING = (2, "Bêtatage en cours")
    BETA_COMPLETE = (3, "Bêtatage réalisé")
    PENDING = (4, "En cours de validation")
    EDIT_REQUIRED = (5, "En attente de modification")
    EDITED = (6, "Modifié")
    PUBLISHED = (7, "Publié")


class CollectionAccess(IntegerChoices):
    """Niveaux d'accès aux séries"""

    CLOSED = (1, "Fermée")
    MODERATED = (2, "Modérée")
    OPEN = (3, "Ouverte")
