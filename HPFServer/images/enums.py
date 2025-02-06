from django.db.models import IntegerChoices
from django.db.models.enums import ChoicesMeta
from enum import IntFlag, auto

class BannerType(IntegerChoices):
    WEBSITE = (1, "Bannière du site")
    PARTNER = (2, "Bannière de partenaire")
    EVENT = (3, "Bannière événementielle")
    PREMIUM = (4, "Bannière d'adhérent")


class FlagChoicesMeta(ChoicesMeta):
    @property
    def combined_choices(cls):
        """Permet à la manière de la méthode .choices d'obtenir la liste des choix combinés"""

        combination_count = (len(ExplicitContent) - 1) ** 2  # -1 pour ne pas tenir compte du SAFE = 0
        extract_labels = lambda i: ", ".join(str(ExplicitContent(i)).split(".")[-1].title().split("|"))
        return [(ExplicitContent(i).value, extract_labels(i)) for i in range(combination_count)]


class ExplicitContent(IntFlag, metaclass=FlagChoicesMeta):
    """\
    Types d'images sensibles, permet des opérations binaires 
    
    IMPORTANT : Risque de confusion en cas de modification :
    - Ne jamais supprimer de type de contenu ou les réordonner
    - En cas de besoin, ajouter un nouvel élément à la suite des autres avec auto()
    """

    SAFE = 0
    MATURE = auto()
    GORE = auto()

    @property
    def label(self):
        return self._label_
