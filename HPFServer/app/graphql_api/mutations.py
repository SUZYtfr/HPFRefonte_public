import django.db.transaction
from django.utils import timezone
from strawberry import Info, cast, auto
import strawberry_django
from strawberry_django.auth.utils import get_current_user
from strawberry_django.permissions import IsAuthenticated
from app.graphql_api.types import NewsCommentType, ChapterType, FictionType, ChapterVersionType
from news.models import NewsComment
from fictions.models import Fiction, Chapter, ChapterVersion


### NEWS

# Inputs

@strawberry_django.input(model=NewsComment)
class NewsCommentInput:
    text: auto


# News
def post_comment(news_article_id: int, comment_data: NewsCommentInput, info: Info) -> NewsCommentType:
    current_user = get_current_user(info)
    comment = NewsComment.objects.create(
        newsarticle_id=news_article_id,
        text=comment_data.text,
        creation_user=current_user,
    )
    return cast(NewsCommentType, comment)


### FICTIONS

# Inputs
@strawberry_django.input(Fiction)
class FictionInput:
    title: auto


@strawberry_django.input(Chapter)
class ChapterInput:
    title: str
    text: str


# Fictions
def create_fiction(
    fiction_data: FictionInput,
    first_chapter_data: ChapterInput,
    info: Info,
) -> FictionType:
    current_user = get_current_user(info)
    with django.db.transaction.atomic():
        fiction = Fiction.objects.create(
            creation_user=current_user,
            title=fiction_data.title,
        )
        first_chapter = Chapter.objects.create(
            fiction=fiction,
            creation_user=current_user,
        )
        first_chapter_version = ChapterVersion.objects.create(
            chapter=first_chapter,
            creation_user=current_user,
            title=first_chapter_data.title,
            text=first_chapter_data.text,
            word_count=20,
        )

    return cast(FictionType, fiction)


def update_fiction(
    fiction_id: int,
    fiction_data: FictionInput,
    info: Info,
) -> FictionType:
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)

    if fiction.creation_user != current_user:
        raise Exception("La fiction n'appartient pas à l'utilisateur authentifié")  # TODO regarder comment fonctionnent les exceptions
    for field, value in vars(fiction_data).items():  # TODO moche
        setattr(fiction, field, value)
    fiction.save()

    return cast(FictionType, fiction)


def delete_fiction(fiction_id: int, info: Info) -> None:
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)
    
    if fiction.creation_user != current_user:
        raise Exception("La fiction n'appartient pas à l'utilisateur authentifié")  # TODO regarder comment fonctionnent les exceptions

    fiction.delete()
    return None


# Chapitres
def create_chapter(
    fiction_id: int,
    chapter_data: ChapterInput,
    info: Info,
) -> ChapterType:
    current_user = get_current_user(info)

    fiction = Fiction.objects.get(pk=fiction_id)

    if fiction.creation_user != current_user:
        raise Exception("La fiction n'appartient pas à l'utilisateur authentifié")  # TODO regarder comment fonctionnent les exceptions

    with django.db.transaction.atomic():
        chapter = Chapter.objects.create(
            fiction_id=fiction_id,
            creation_user=current_user,
        )
        chapter_version = ChapterVersion.objects.create(
            chapter=chapter,
            creation_user=current_user,
            title=chapter_data.title,
            text=chapter_data.text,
            word_count=20,
        )

    return cast(ChapterType, chapter)


def update_chapter(
    chapter_id: int,
    chapter_data: ChapterInput,
    info: Info,
) -> ChapterType:
    current_user = get_current_user(info)

    chapter = Chapter.objects.get(pk=chapter_id)

    if chapter.creation_user != current_user:
        raise Exception("Le chapitre n'appartient pas à l'utilisateur authentifié")  # TODO regarder comment fonctionnent les exceptions

    with django.db.transaction.atomic():
        # TODO peut-être des champs à Chapter ici ?
        chapter_version = ChapterVersion.objects.create(
            chapter=chapter,
            creation_user=current_user,
            title=chapter_data.title,
            text=chapter_data.text,
            word_count=20,
        )

    # TODO faut-il rafraîchir chapter ?
    return cast(ChapterType, chapter)


def delete_chapter(
    chapter_id: int,
    info: Info,
) -> None:
    current_user = get_current_user(info)
    chapter = Chapter.objects.get(pk=chapter_id)
    
    if chapter.creation_user != current_user:
        raise Exception("Le chapitre n'appartient pas à l'utilisateur authentifié")  # TODO regarder comment fonctionnent les exceptions

    fiction = chapter.fiction
    with django.db.transaction.atomic():
        chapter.delete()
        fiction.refresh_from_db()
        if fiction.chapters.count() == 0:
            fiction.delete()

    return None




### ADMIN

### Inputs
@strawberry_django.input(model=ChapterVersion)  # seulement les champs concernés
class InvalidationInput:
    public_comment: auto
    private_comment: auto
    invalidation_reasons: list[int]
    to_be_discussed: auto


### Fictions

def invalidate_chapter_version(
    chapter_version_id: int,
    invalidation_data: InvalidationInput,
    info: Info,
) -> ChapterVersionType:
    current_user = get_current_user(info)
    chapter_version = ChapterVersion.objects.get(pk=chapter_version_id)

    # vérification
    if chapter_version.is_draft:
        raise Exception("Invalidation impossible : La version de texte est un brouillon.")
    if chapter_version != chapter_version.chapter.last_version \
        and chapter_version != chapter_version.chapter.published_version:
        raise Exception("Invalidation impossible : La version de texte n'est pas une version publiée ou de travail.")

    # mutation
    with django.db.transaction.atomic():
        for field, value in vars(invalidation_data).items():
            if field == "invalidation_reasons": continue  # TODO moche
            setattr(chapter_version, field, value)
            chapter_version.invalidation_date = timezone.now()
            chapter_version.invalidation_user = current_user
            chapter_version.save()
        chapter_version.invalidation_reasons.set(invalidation_data.invalidation_reasons)

    return cast(ChapterVersionType, chapter_version)
