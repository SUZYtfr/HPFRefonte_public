import django.db.transaction
from django.utils import timezone
import strawberry
from strawberry import Info, cast, auto
import strawberry_django
from strawberry_django.auth.utils import get_current_user
from strawberry_django.permissions import IsAuthenticated, IsStaff
from strawberry_django_extras import JWTMutations
from app.graphql_api.types import *
from app.graphql_api.inputs import NewsCommentInput, FictionInput, ChapterInput, InvalidationInput
from app.graphql_api.exceptions import NotOwnerError, NotOwnerOrStaffError
from news.models import NewsComment
from fictions.models import Fiction, Chapter, ChapterVersion


### NEWS
def post_comment(news_article_id: int, comment_data: NewsCommentInput, info: Info) -> NewsCommentType:
    # récupération
    current_user = get_current_user(info)
    
    # mutation
    comment = NewsComment.objects.create(
        newsarticle_id=news_article_id,
        text=comment_data.text,
        creation_user=current_user,
        modification_user=current_user,
    )
    return cast(NewsCommentType, comment)


### FICTIONS
def create_fiction(
    fiction_data: FictionInput,
    first_chapter_data: ChapterInput,
    info: Info,
) -> FictionType:
    # récupération
    current_user = get_current_user(info)
    
    # mutation
    with django.db.transaction.atomic():
        fiction = Fiction.objects.create(
            creation_user=current_user,
            modification_user=current_user,
            title=fiction_data.title,
        )
        first_chapter = Chapter.objects.create(
            fiction=fiction,
            creation_user=current_user,
            modification_user=current_user,
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
    # récupération
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)

    # vérification
    if fiction.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError
    
    # mutation
    for field, value in vars(fiction_data).items():  # TODO moche
        setattr(fiction, field, value)
        fiction.modification_user = current_user
    fiction.save()
    # TODO m2m
    return cast(FictionType, fiction)


def delete_fiction(fiction_id: int, info: Info) -> None:
    # récupération
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)
    
    # vérification
    if fiction.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    fiction.delete()
    return None


# Chapitres
def create_chapter(
    fiction_id: int,
    chapter_data: ChapterInput,
    info: Info,
) -> ChapterType:
    # récupération
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)

    # vérification
    if fiction.creation_user != current_user:
        raise NotOwnerError

    # mutation
    # TODO est-ce qu'on update modification_user sur fiction?
    with django.db.transaction.atomic():
        chapter = Chapter.objects.create(
            fiction_id=fiction_id,
            creation_user=current_user,
            modification_user=current_user,
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
    # récupération
    current_user = get_current_user(info)
    chapter = Chapter.objects.get(pk=chapter_id)

    # vérification
    if chapter.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    with django.db.transaction.atomic():
        # TODO peut-être des champs à Chapter ici ?
        # TODO est-ce qu'on update update.modification_user ?
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
    # récupération
    current_user = get_current_user(info)
    chapter = Chapter.objects.get(pk=chapter_id)
    
    # vérification
    if chapter.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    fiction = chapter.fiction
    with django.db.transaction.atomic():
        chapter.delete()
        fiction.refresh_from_db()
        if fiction.chapters.count() == 0:
            fiction.delete()

    return None


### ADMIN

### Fictions
def invalidate_chapter_version(
    chapter_version_id: int,
    invalidation_data: InvalidationInput,
    info: Info,
) -> ChapterVersionType:
    # récupération
    current_user = get_current_user(info)
    chapter_version = ChapterVersion.objects.get(pk=chapter_version_id)

    # vérification
    if not chapter_version.submission_date:
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


@strawberry.type
class Mutation:
    # publique
    request_token = JWTMutations.issue

    # privé
    post_comment = strawberry_django.mutation(
        resolver=post_comment,
        extensions=[IsAuthenticated()],
    )
    create_fiction = strawberry_django.mutation(
        resolver=create_fiction,
        extensions=[IsAuthenticated()],
    )
    update_fiction = strawberry_django.mutation(
        resolver=update_fiction,
        extensions=[IsAuthenticated()],
    )
    delete_fiction = strawberry_django.mutation(
        resolver=delete_fiction,
        extensions=[IsAuthenticated()],
    )
    create_chapter = strawberry_django.mutation(
        resolver=create_chapter,
        extensions=[IsAuthenticated()],
    )
    update_chapter = strawberry_django.mutation(
        resolver=update_chapter,
        extensions=[IsAuthenticated()],
    )
    delete_chapter = strawberry_django.mutation(
        resolver=delete_chapter,
        extensions=[IsAuthenticated()],
    )

    # admin
    invalidate_chapter_version = strawberry_django.mutation(
        resolver=invalidate_chapter_version,
        extensions=[IsStaff()],
    )
