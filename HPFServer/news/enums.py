from django.db.models import IntegerChoices


class NewsStatus(IntegerChoices):
    """Statuts de publication des actualités"""

    PENDING = (1, "En attente")
    DRAFT = (2, "À publier")
    PUBLISHED = (3, "Publiée")


class NewsCategory(IntegerChoices):
    """Catégories des actualités"""

    UNDEFINED = (0, "Actualité")
    ASSEMBLY = (1, "Assemblée générale")
    ASSOCIATION = (2, "Association")
    CONTEST = (3, "Concours")
    NIGHTS = (4, "Nuits")
    PODIUM = (5, "Podium")
    PROJECTS = (6, "Projet")
