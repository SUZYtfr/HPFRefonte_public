from strawberry import Info
from strawberry_django.permissions import DjangoPermissionExtension, DjangoNoPermission, _desc

from graphql.pyutils import AwaitableOrValue
from typing import TYPE_CHECKING, ClassVar, Optional, Callable, Any

if TYPE_CHECKING:
    from app.graphql_api.types import UserType


# NOTE : ne peut pas être utilisé sans "source", donc pas comme extension de mutation par ex.
class IsStaffOrOwner(DjangoPermissionExtension):
    """Vérifie que l'utilisateur accédant à la ressource est un modérateur ou le propriétaire de la ressource"""

    DEFAULT_ERROR_MESSAGE: ClassVar[str] = "L'utilisateur n'est pas un modérateur ou propriétaire de la ressource."
    SCHEMA_DIRECTIVE_DESCRIPTION: ClassVar[Optional[str]] = _desc(
        "Ne peut être résolu que par un modérateur ou le propriétaire de la ressource.",
    )

    # le champ de la source contre lequel la propriété est vérifiée
    _owner_field: str

    def __init__(self, *, message: str | None = None, use_directives: bool = True, fail_silently: bool = True, owner_field: str | None = None) -> None:
        if owner_field is None:
            raise Exception("Le champ de propriété de la source doit être indiqué.")
        self._owner_field = owner_field
        super().__init__(message=message, use_directives=use_directives, fail_silently=fail_silently)

    def resolve_for_user(self, resolver: Callable, user: Optional["UserType"], *, info: Info, source: Any) -> AwaitableOrValue[Any]:
        if (
            user is None
            or not user.is_authenticated
            or (not getattr(user, "is_staff", False) and not getattr(source, self._owner_field) == user)
        ):
            raise DjangoNoPermission

        return resolver()
