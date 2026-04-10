import django.db.transaction
from django.utils import timezone
import strawberry
from strawberry import Info, cast
import strawberry_django
from strawberry_django.auth.utils import get_current_user
from strawberry_django.permissions import IsAuthenticated, IsStaff
from strawberry_django_extras.jwt.mutations import JWTMutations
from app.graphql_api.types import (
    NewsCommentType,
    CollectionType,
    CollectionItemType,
    FictionType,
    ChapterType,
    ChapterVersionType,
    ChapterReviewType,
    FictionReviewType,
    CollectionReviewType,
)
from app.graphql_api.inputs import (
    NewsCommentInput,
    FictionInput,
    ChapterInput,
    InvalidationInput,
    ReviewInput,
    CollectionInput,
    CollectionItemInput,
)
from app.graphql_api.exceptions import NotOwnerError, NotOwnerOrStaffError
from news.models import NewsComment
from fictions.models import (
    Fiction,
    Chapter,
    ChapterVersion,
    Collection,
    CollectionItem,
    ChapterCollectionItem,
    FictionCollectionItem,
    CollectionCollectionItem,
)
from reviews.models import ChapterReview, FictionReview, CollectionReview
from core.text_functions import count_words


### NEWS
def post_comment(
    info: Info,
    news_article_id: strawberry.ID,
    comment_data: NewsCommentInput,
) -> NewsCommentType:
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
    info: Info,
    fiction_data: FictionInput,
    first_chapter_data: ChapterInput,
) -> FictionType:
    # récupération
    current_user = get_current_user(info)

    # mutation
    word_count = count_words(first_chapter_data.text)
    if not first_chapter_data.is_draft:  # TODO - and user.has_auto_publish
        publication_date = timezone.now()
    else:
        publication_date = None

    with django.db.transaction.atomic():
        fiction = Fiction.objects.create(
            creation_user=current_user,
            modification_user=current_user,
            title=fiction_data.title,
            summary=fiction_data.summary,
            storynote=fiction_data.storynote,
            status=fiction_data.status,
            rating=fiction_data.rating,
            last_update_date=publication_date,
        )

        if fiction_data.fandoms:
            if fiction_data.fandoms.add:
                fiction.fandoms.add(*fiction_data.fandoms.add)
            if fiction_data.fandoms.remove:
                fiction.fandoms.remove(*fiction_data.fandoms.remove)
            if fiction_data.fandoms.set == []:
                fiction.fandoms.clear()
            if fiction_data.fandoms.set:
                fiction.fandoms.set(fiction_data.fandoms.set)

        if fiction_data.characteristics:
            if fiction_data.characteristics.add:
                fiction.characteristics.add(*fiction_data.characteristics.add)
            if fiction_data.characteristics.remove:
                fiction.characteristics.remove(*fiction_data.characteristics.remove)
            if fiction_data.characteristics.set == []:
                fiction.characteristics.clear()
            if fiction_data.characteristics.set:
                fiction.characteristics.set(fiction_data.characteristics.set)

        chapter = Chapter.objects.create(
            fiction=fiction,
            creation_user=current_user,
            modification_user=current_user,
            title=first_chapter_data.title,
            text=first_chapter_data.text,
            start_note=first_chapter_data.start_note,
            end_note=first_chapter_data.end_note,
            word_count=word_count,
            publication_date=publication_date,
        )

        if first_chapter_data.trigger_warnings:
            if first_chapter_data.trigger_warnings.add:
                chapter.trigger_warnings.add(*first_chapter_data.trigger_warnings.add)
            if first_chapter_data.trigger_warnings.remove:
                chapter.trigger_warnings.remove(
                    *first_chapter_data.trigger_warnings.remove,
                )
            if first_chapter_data.trigger_warnings.set == []:
                chapter.trigger_warnings.clear()
            if first_chapter_data.trigger_warnings.set:
                chapter.trigger_warnings.set(first_chapter_data.trigger_warnings.set)

        if not first_chapter_data.is_draft:
            chapter_version = ChapterVersion.objects.create(
                chapter=chapter,
                creation_user=current_user,
                title=first_chapter_data.title,
                text=first_chapter_data.text,
                start_note=first_chapter_data.start_note,
                end_note=first_chapter_data.end_note,
                word_count=word_count,
                submission_date=publication_date,
            )
            chapter.published_version = chapter_version
            chapter.save()

    fiction.refresh_from_db()
    return cast(FictionType, fiction)


def update_fiction(
    info: Info,
    fiction_id: strawberry.ID,
    fiction_data: FictionInput,
) -> FictionType:
    # récupération
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)

    # vérification
    if fiction.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    fiction.modification_user = current_user
    fiction.title = fiction_data.title
    fiction.summary = fiction_data.summary
    fiction.storynote = fiction_data.storynote
    fiction.status = fiction_data.status
    fiction.rating = fiction_data.rating
    fiction.save()

    if fiction_data.fandoms:
        if fiction_data.fandoms.add:
            fiction.fandoms.add(*fiction_data.fandoms.add)
        if fiction_data.fandoms.remove:
            fiction.fandoms.remove(*fiction_data.fandoms.remove)
        if fiction_data.fandoms.set == []:
            fiction.fandoms.clear()
        if fiction_data.fandoms.set:
            fiction.fandoms.set(fiction_data.fandoms.set)

    if fiction_data.characteristics:
        if fiction_data.characteristics.add:
            fiction.characteristics.add(*fiction_data.characteristics.add)
        if fiction_data.characteristics.remove:
            fiction.characteristics.remove(*fiction_data.characteristics.remove)
        if fiction_data.characteristics.set == []:
            fiction.characteristics.clear()
        if fiction_data.characteristics.set:
            fiction.characteristics.set(fiction_data.characteristics.set)

    return cast(FictionType, fiction)


def delete_fiction(info: Info, fiction_id: strawberry.ID) -> None:
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
    info: Info,
    fiction_id: strawberry.ID,
    chapter_data: ChapterInput,
) -> ChapterType:
    # récupération
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)

    # vérification
    if fiction.creation_user != current_user:
        raise NotOwnerError

    # mutation
    word_count = count_words(chapter_data.text)
    if not chapter_data.is_draft:  # TODO - and user.has_auto_publish
        publication_date = timezone.now()
    else:
        publication_date = None

    with django.db.transaction.atomic():
        chapter = Chapter.objects.create(
            fiction_id=fiction_id,
            creation_user=current_user,
            modification_user=current_user,
            title=chapter_data.title,
            text=chapter_data.text,
            start_note=chapter_data.start_note,
            end_note=chapter_data.end_note,
            word_count=word_count,
            publication_date=publication_date,
        )

        if chapter_data.trigger_warnings:
            if chapter_data.trigger_warnings.add:
                chapter.trigger_warnings.add(*chapter_data.trigger_warnings.add)
            if chapter_data.trigger_warnings.remove:
                chapter.trigger_warnings.remove(*chapter_data.trigger_warnings.remove)
            if chapter_data.trigger_warnings.set == []:
                chapter.trigger_warnings.clear()
            if chapter_data.trigger_warnings.set:
                chapter.trigger_warnings.set(chapter_data.trigger_warnings.set)

        if not chapter_data.is_draft:  # TODO - and user.has_auto_publish:
            chapter_version = ChapterVersion.objects.create(
                chapter=chapter,
                creation_user=current_user,
                title=chapter_data.title,
                text=chapter_data.text,
                start_note=chapter_data.start_note,
                end_note=chapter_data.end_note,
                word_count=word_count,
                submission_date=publication_date,
            )
            chapter.published_version = chapter_version
            chapter.save()

            chapter.fiction.last_update_date = publication_date
            chapter.fiction.save()

    return cast(ChapterType, chapter)


def update_chapter(
    info: Info,
    chapter_id: strawberry.ID,
    chapter_data: ChapterInput,
) -> ChapterType:
    # récupération
    current_user = get_current_user(info)
    chapter = Chapter.objects.get(pk=chapter_id)

    # vérification
    if chapter.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    if chapter.is_published() and chapter_data.is_draft:
        msg = "Le chapitre et publié et ne peut être passé en brouillon"
        raise ValueError(msg)

    # mutation
    is_publishing = not chapter.is_published() and not chapter_data.is_draft

    if not chapter_data.is_draft:  # TODO - and user.has_auto_publish
        publication_date = timezone.now()
    else:
        publication_date = chapter.publication_date
    word_count = count_words(chapter_data.text)

    with django.db.transaction.atomic():
        chapter.modification_user = current_user
        chapter.title = chapter_data.title
        chapter.text = chapter_data.text
        chapter.start_note = chapter_data.start_note
        chapter.end_note = chapter_data.end_note
        chapter.word_count = word_count
        chapter.publication_date = publication_date

        if chapter_data.trigger_warnings:
            if chapter_data.trigger_warnings.add:
                chapter.trigger_warnings.add(*chapter_data.trigger_warnings.add)
            if chapter_data.trigger_warnings.remove:
                chapter.trigger_warnings.remove(*chapter_data.trigger_warnings.remove)
            if chapter_data.trigger_warnings.set == []:
                chapter.trigger_warnings.clear()
            if chapter_data.trigger_warnings.set:
                chapter.trigger_warnings.set(chapter_data.trigger_warnings.set)

        if not chapter_data.is_draft:  # TODO - and user.has_auto_publish:
            chapter_version = ChapterVersion.objects.create(
                chapter=chapter,
                creation_user=current_user,
                title=chapter_data.title,
                text=chapter_data.text,
                word_count=word_count,
                start_note=chapter_data.start_note,
                end_note=chapter_data.end_note,
            )
            chapter.published_version = chapter_version
            chapter.save()

        if is_publishing:
            chapter.fiction.last_update_date = publication_date
            chapter.fiction.save()

    chapter.refresh_from_db()
    return cast(ChapterType, chapter)


def delete_chapter(
    info: Info,
    chapter_id: strawberry.ID,
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


# Séries


def create_collection(
    info: Info,
    collection_data: CollectionInput,
) -> CollectionType:
    # récupération
    current_user = get_current_user(info)

    # mutation
    with django.db.transaction.atomic():
        collection = Collection.objects.create(
            creation_user=current_user,
            modification_user=current_user,
            title=collection_data.title,
            summary=collection_data.summary,
            access=collection_data.access,
        )

        if collection_data.fandoms:
            if collection_data.fandoms.add:
                collection.fandoms.add(*collection_data.fandoms.add)
            if collection_data.fandoms.remove:
                collection.fandoms.remove(*collection_data.fandoms.remove)
            if collection_data.fandoms.set == []:
                collection.fandoms.clear()
            if collection_data.fandoms.set:
                collection.fandoms.set(collection_data.fandoms.set)

        if collection_data.characteristics:
            if collection_data.characteristics.add:
                collection.characteristics.add(*collection_data.characteristics.add)
            if collection_data.characteristics.remove:
                collection.characteristics.remove(
                    *collection_data.characteristics.remove,
                )
            if collection_data.characteristics.set == []:
                collection.characteristics.clear()
            if collection_data.characteristics.set:
                collection.characteristics.set(collection_data.characteristics.set)

    return cast(CollectionType, collection)


def update_collection(
    info: Info,
    collection_id: strawberry.ID,
    collection_data: CollectionInput,
) -> CollectionType:
    # récupération
    current_user = get_current_user(info)
    collection = Collection.objects.get(pk=collection_id)

    # vérification
    if collection.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    with django.db.transaction.atomic():
        collection.modification_user = current_user
        collection.title = collection_data.title
        collection.summary = collection_data.summary
        collection.access = collection_data.access
        collection.save()

        if collection_data.fandoms:
            if collection_data.fandoms.add:
                collection.fandoms.add(*collection_data.fandoms.add)
            if collection_data.fandoms.remove:
                collection.fandoms.remove(*collection_data.fandoms.remove)
            if collection_data.fandoms.set == []:
                collection.fandoms.clear()
            if collection_data.fandoms.set:
                collection.fandoms.set(collection_data.fandoms.set)

        if collection_data.characteristics:
            if collection_data.characteristics.add:
                collection.characteristics.add(*collection_data.characteristics.add)
            if collection_data.characteristics.remove:
                collection.characteristics.remove(
                    *collection_data.characteristics.remove,
                )
            if collection_data.characteristics.set == []:
                collection.characteristics.clear()
            if collection_data.characteristics.set:
                collection.characteristics.set(collection_data.characteristics.set)

    return cast(CollectionType, collection)


def create_collection_item(
    info: Info,
    collection_id: strawberry.ID,
    collection_item_data: CollectionItemInput,
) -> list[CollectionItemType]:
    # récupération
    current_user = get_current_user(info)
    parent_collection: Collection = Collection.objects.get(pk=collection_id)

    # vérification
    if parent_collection.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    if chapter_id := getattr(collection_item_data, "chapter_id", None):
        if ChapterCollectionItem.objects.filter(
            parent=parent_collection,
            chapter_id=chapter_id.value,
        ):
            msg = "La série parente contient déjà le chapitre"
            raise ValueError(msg)

        ChapterCollectionItem.objects.create(
            parent=parent_collection,
            chapter_id=chapter_id.value,
            is_accepted=True,
            addition_user=current_user,
        )
    elif fiction_id := getattr(collection_item_data, "fiction_id", None):
        if FictionCollectionItem.objects.filter(
            parent=parent_collection,
            fiction_id=fiction_id.value,
        ):
            msg = "La série parente contient déjà la fiction"
            raise ValueError(msg)

        FictionCollectionItem.objects.create(
            parent=parent_collection,
            fiction_id=fiction_id.value,
            is_accepted=True,
            addition_user=current_user,
        )
    elif collection_id := getattr(collection_item_data, "collection_id", None):
        if CollectionCollectionItem.objects.filter(
            parent=parent_collection,
            collection_id=collection_id.value,
        ):
            msg = "La série parente contient déjà la série"
            raise ValueError(msg)

        CollectionCollectionItem.objects.create(
            parent=parent_collection,
            collection_id=collection_id.value,
            is_accepted=True,
            addition_user=current_user,
        )

    return cast(CollectionItemType, parent_collection.items.all())


def accept_collection_item(
    info: Info,
    collection_item_id: strawberry.ID,
) -> list[CollectionItemType]:
    # récupération
    current_user = get_current_user(info)
    collection_item: CollectionItem = CollectionItem.objects.get(pk=collection_item_id)
    collection: Collection = collection_item.parent

    # vérification
    if collection.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    collection_item.is_accepted = True
    collection_item.save()

    return cast(CollectionItemType, collection.items.all())


def move_collection_item(
    info: Info,
    collection_item_id: strawberry.ID,
    new_position: int,
) -> list[CollectionItemType]:
    # récupération
    current_user = get_current_user(info)
    collection_item: CollectionItem = CollectionItem.objects.get(pk=collection_item_id)
    collection: Collection = collection_item.parent

    # vérification
    if collection.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    collection_item.to(new_position)

    return cast(CollectionItemType, collection.items.all())


def delete_collection_item(
    info: Info,
    collection_item_id: strawberry.ID,
) -> list[CollectionItemType]:
    # récupération
    current_user = get_current_user(info)
    collection_item: CollectionItem = CollectionItem.objects.get(pk=collection_item_id)
    collection: Collection = collection_item.parent

    # vérification
    if collection.creation_user != current_user and not current_user.is_staff:
        raise NotOwnerOrStaffError

    # mutation
    collection_item.delete()

    return cast(CollectionItemType, collection.items.all())


### REVIEWS


def create_fiction_review(
    info: Info,
    fiction_id: strawberry.ID,
    review_data: ReviewInput,
) -> FictionReviewType:
    current_user = get_current_user(info)
    fiction = Fiction.objects.get(pk=fiction_id)

    # TODO vérifier les conditions de reviews ici
    fiction_review = FictionReview.objects.create(
        **vars(review_data),
        creation_user=current_user,
        fiction=fiction,
        is_draft=False,
        publication_date=timezone.now(),
    )

    return cast(FictionReviewType, fiction_review)


def create_chapter_review(
    info: Info,
    chapter_id: strawberry.ID,
    review_data: ReviewInput,
) -> ChapterReviewType:
    current_user = get_current_user(info)
    chapter = Chapter.objects.get(pk=chapter_id)

    # TODO vérifier les conditions de reviews ici
    chapter_review = ChapterReview.objects.create(
        **vars(review_data),
        creation_user=current_user,
        chapter=chapter,
        is_draft=False,
        publication_date=timezone.now(),
    )

    return cast(ChapterReviewType, chapter_review)


def create_collection_review(
    info: Info,
    collection_id: strawberry.ID,
    review_data: ReviewInput,
) -> CollectionReviewType:
    current_user = get_current_user(info)
    collection = Collection.objects.get(pk=collection_id)

    # TODO vérifier les conditions de reviews ici
    collection_review = CollectionReview.objects.create(
        **vars(review_data),
        creation_user=current_user,
        collection=collection,
        is_draft=False,
        publication_date=timezone.now(),
    )

    return cast(CollectionReviewType, collection_review)


### ADMIN


### Fictions
def invalidate_chapter_version(
    info: Info,
    chapter_version_id: strawberry.ID,
    invalidation_data: InvalidationInput,
) -> ChapterVersionType:
    # récupération
    current_user = get_current_user(info)
    chapter_version = ChapterVersion.objects.get(pk=chapter_version_id)

    # vérification
    if not chapter_version.submission_date:
        msg = "Invalidation impossible : La version de texte est un brouillon."
        raise Exception(msg)
    if (
        chapter_version != chapter_version.chapter.last_version
        and chapter_version != chapter_version.chapter.published_version
    ):
        msg = "Invalidation impossible : La version de texte n'est pas une version publiée ou de travail."
        raise Exception(msg)

    # mutation
    with django.db.transaction.atomic():
        for field, value in vars(invalidation_data).items():
            if field == "invalidation_reasons":
                continue  # TODO moche  #noqa:E701
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
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    create_fiction = strawberry_django.mutation(
        resolver=create_fiction,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    update_fiction = strawberry_django.mutation(
        resolver=update_fiction,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    delete_fiction = strawberry_django.mutation(
        resolver=delete_fiction,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    create_chapter = strawberry_django.mutation(
        resolver=create_chapter,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    update_chapter = strawberry_django.mutation(
        resolver=update_chapter,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    delete_chapter = strawberry_django.mutation(
        resolver=delete_chapter,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    create_fiction_review = strawberry_django.mutation(
        resolver=create_fiction_review,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    create_chapter_review = strawberry_django.mutation(
        resolver=create_chapter_review,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    create_collection_review = strawberry_django.mutation(
        resolver=create_collection_review,
        extensions=[IsAuthenticated(fail_silently=False)],
    )

    # série
    create_collection = strawberry.mutation(
        resolver=create_collection,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    update_collection = strawberry.mutation(
        resolver=update_collection,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    create_collection_item = strawberry.mutation(
        resolver=create_collection_item,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    accept_collection_item = strawberry.mutation(
        resolver=accept_collection_item,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    move_collection_item = strawberry.mutation(
        resolver=move_collection_item,
        extensions=[IsAuthenticated(fail_silently=False)],
    )
    delete_collection_item = strawberry_django.mutation(
        resolver=delete_collection_item,
        extensions=[IsAuthenticated(fail_silently=False)],
    )

    # admin
    invalidate_chapter_version = strawberry_django.mutation(
        resolver=invalidate_chapter_version,
        extensions=[IsStaff()],
    )
