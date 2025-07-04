from strawberry import Info
from fictions.models import Fiction, Chapter


def resolve_public_fictions():
    return Fiction.objects.published()


def resolve_public_chapters():
    return Chapter.objects.published()

