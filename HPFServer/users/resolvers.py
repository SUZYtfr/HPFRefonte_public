
from django.db.models import QuerySet
from users.models import User


def resolve_users(root, info) -> QuerySet[User]:
    return User.objects.all()

def resolve_user(root, info, id: int) -> User:
    return User.objects.get(pk=id)
