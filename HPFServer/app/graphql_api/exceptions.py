class InsufficientRightError(Exception):
    default_message = "L'utilisateur n'a pas les droits suffisants"

    def __init__(self, msg: str | None = None, *args, **kwargs) -> None:
        if not msg:
            msg = self.default_message
        super().__init__(msg, *args, **kwargs)


class NotOwnerError(InsufficientRightError):
    default_message = "L'utilisateur n'est pas le propriétaire de la ressource"


class NotOwnerOrStaffError(InsufficientRightError):
    default_message = "L'utilisateur n'est ni modérateur ni propriétaire de la ressource"
