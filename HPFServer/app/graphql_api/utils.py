from django.db.models import Count
from strawberry_django_extras.jwt.utils import jwt_payload

from users.models import User

from typing import Any


"""
TODO définir une politique de ce qui passe dans le payload du jeton JWT.
Il est tentant d'y mettre le profil utilisateur, pour ne plus avoir besoin d'un
deuxième appel suivant le login, et d'éviter un scénario : appel login réussi, appel profil raté.
D'un autre côté, tout ajout alourdit le jeton, qui accompagne chaque requête.
"""
def get_jwt_token_payload(user: User) -> dict[str, Any]:
    base_payload = jwt_payload(user)
    extra_payload = {
        "username": user.username,
        "userId": user.pk,
        "isStaff": user.is_staff,
        "preferred5Fandoms": list(
            (
                user.created_fictions.values("fandoms")
                .annotate(Count("fandoms"))
                .order_by("-fandoms__count")
                .values_list("fandoms", flat=True)[:5]
            ),
        ),
    }

    return {**base_payload, **extra_payload}

