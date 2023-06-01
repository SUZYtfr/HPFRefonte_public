from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.hashers import make_password


def get_moderation_account():
    """Renvoie le compte de modération"""

    moderation_accout, created = get_user_model().objects.get_or_create(
        pk=settings.MODERATION_ACCOUNT["pk"],
        defaults={
            "username": settings.MODERATION_ACCOUNT["username"],
            "email": settings.MODERATION_ACCOUNT["email"],
            "password": make_password(None),
        },
    )

    return moderation_accout


# En cas de suppression pure et dure d'un compte créateur ou modificateur d'un élément, remplacement par la sentinelle
# Permet de conserver par exemple une fiction dont le créateur supprimant son compte n'était plus l'auteur
# Cette sentinelle concerne la BBD, les règles d'autorat sont déterminées au niveau des modèles
def get_user_deleted_sentinel():
    """Renvoie le compte sentinelle"""

    deleted_sentinel, created = get_user_model().objects.get_or_create(
        pk=settings.ANONYMOUS_ACCOUNT["pk"],
        defaults={
            "username": settings.ANONYMOUS_ACCOUNT["username"],
            "email": settings.ANONYMOUS_ACCOUNT["email"],
            "password": make_password(None),
        },
    )

    return deleted_sentinel
