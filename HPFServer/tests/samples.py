import faker
import lorem
import time
import datetime
import random

from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone

from users.models import User
from characteristics.models import Characteristic, CharacteristicType
from fictions.models import Fiction, Chapter, Collection, ChapterValidationStage
from reviews.models import FictionReview, ChapterReview, CollectionReview
from news.models import NewsArticle, NewsComment, NewsStatus


french_faker = faker.Faker("fr_FR")


def random_characteristic_type():
    if CharacteristicType.objects.count() > 0:
        return random.choices(list(CharacteristicType.objects.all()))[0]
    else:
        return sample_characteristic_type()


def random_date():
    d = random.randint(1, int(time.time()))
    return datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d')


def get_random_user():
    return User.objects.exclude(pk__lte=0).order_by("?").first()


# MODÈLES AUTO-GÉNÉRÉS

def sample_user(**kwargs):
    user = User.objects.create_user(
        username=kwargs.pop("username", None) or french_faker.user_name(),
        email=kwargs.pop("email", None) or french_faker.email(safe=True),
        password=kwargs.pop("password", None) or make_password(None),  # mot de passe inutilisable
        realname=kwargs.pop("realname", None) or french_faker.name(),
        birthdate=kwargs.pop("birthdate", None) or french_faker.date_of_birth(),
        bio=kwargs.pop("bio", None) or french_faker.paragraph(3),
        gender=kwargs.pop("gender", None) or french_faker.random_int(min=0, max=3),
    )
    return user


def sample_fiction(generate_chapters=None, **kwargs):
    with transaction.atomic():
        fiction = Fiction.objects.create(
            creation_user=kwargs.pop("creation_user", None) or get_random_user(),
            title=kwargs.pop("title", None) or french_faker.sentence(),
            summary=kwargs.pop("summary", None) or french_faker.paragraph(10),
            storynote=kwargs.pop("storynote", None) or french_faker.paragraph(10),
            status=kwargs.pop("status", None) or french_faker.random_int(1, 4),
            featured=kwargs.pop("featured", None) or french_faker.boolean(),
            **kwargs,
        )

        random_characteristics = []

        for characteristic_type in CharacteristicType.objects.all():
            min_limit = characteristic_type.min_limit
            max_limit = characteristic_type.max_limit or 5
            random_chartype_chars = set()
            while len(random_chartype_chars) < french_faker.random_int(min_limit, max_limit):
                random_chartype_chars.add(characteristic_type.characteristics.filter(is_forbidden=False).order_by("?").first())
            random_characteristics.extend(random_chartype_chars)

        fiction.characteristics.set(random_characteristics)

        for i in range(1, generate_chapters or french_faker.random_int(1, 5)):
            chapter = Chapter.objects.create(
                creation_user=fiction.creation_user,
                fiction=fiction,
                title=french_faker.sentence(),
                startnote=french_faker.paragraph(10),
                endnote=french_faker.paragraph(10),
                validation_status=ChapterValidationStage.PUBLISHED,
            )
            chapter.create_text_version(
                creation_user=chapter.creation_user,
                text=french_faker.paragraph(100),
                touch=False,
            )
    return fiction


def sample_chapter(creation_user=None, title=None, fiction=None, text=None,
                   **extra_fields):
    if not creation_user:
        creation_user = sample_user()
    if not fiction:
        fiction = sample_fiction(creation_user=creation_user)
    chapter = Chapter.objects.create(
        creation_user=creation_user,
        title=lorem.get_sentence() if title is None else title,
        fiction=fiction,
        **extra_fields
    )
    chapter.create_text_version(text=text or lorem.get_paragraph(3), creation_user=creation_user, touch=False)

    return chapter


def sample_collection(creation_user=None, title=None, summary=None,
                      **extra_fields):
    creation_user = creation_user or sample_user()
    collection = Collection.objects.create(
        creation_user=creation_user,
        title=lorem.get_sentence() if title is None else title,
        summary=lorem.get_paragraph() if summary is None else summary,
        # starting_chapters=[sample_chapter(creation_user=creation_user)] if starting_chapters is None else starting_chapters,
        **extra_fields
    )

    return collection


def sample_characteristic_type(creation_user=None, name=None, min_limit=None, max_limit=None, is_closed=False, **extra_fields):
    if not min_limit or max_limit:
        min_limit, max_limit = sorted(random.choices(range(0, 10), k=2))
    elif min_limit:
        max_limit = random.randint(min_limit, 10)
    elif max_limit:
        min_limit = random.randint(0, max_limit)

    characteristic_type = CharacteristicType.objects.create(
        creation_user=creation_user or User.objects.get(pk=settings.MODERATION_ACCOUNT_ID),
        name=lorem.get_word(3) if name is None else name,
        min_limit=min_limit,
        max_limit=max_limit,
        is_closed=is_closed,
        **extra_fields,
    )
    return characteristic_type


def sample_feature(characteristic_type=None, creation_user=None, name=None,
                   **extra_fields):
    feature = Characteristic.objects.create(
        creation_user=creation_user or User.objects.get(pk=settings.MODERATION_ACCOUNT_ID),
        characteristic_type=characteristic_type or sample_characteristic_type(),
        name=lorem.get_word(3) if name is None else name,
        **extra_fields
    )
    return feature


def sample_fiction_review(**kwargs):
    if fiction_id := kwargs.pop("fiction_id", None):
        pass
    else:
        fiction_id = sample_fiction().id

    if creation_user_id := kwargs.pop("creation_user_id", None):
        creation_user = User.objects.get(id=creation_user_id)
    else:
        creation_user = get_random_user()

    fiction_review = FictionReview.objects.create(
        fiction_id=fiction_id,
        creation_user=creation_user,
        draft=kwargs.pop("draft", False),
        grading=kwargs.pop("grading", None) or french_faker.random_int(min=1, max=10),
        text=kwargs.pop("text", None) or french_faker.paragraph(2),
        **kwargs,
    )
    return fiction_review


def sample_news(**kwargs):
    news_article = NewsArticle.objects.create(
        creation_user=kwargs.pop("creation_user", None) or get_random_user(),
        title=kwargs.pop("title", None) or french_faker.paragraph(),
        content=kwargs.pop("content", None) or french_faker.paragraph(10),
        category=kwargs.pop("category", None) or french_faker.random_int(min=0, max=6),
        status=kwargs.pop("status", None) or NewsStatus.PUBLISHED,
        post_date=kwargs.pop("post_date", None) or timezone.now(),
        **kwargs,
    )
    news_article.authors.add(news_article.creation_user)

    return news_article


def sample_comment(**kwargs):
    comment = NewsComment.objects.create(
        creation_user_id=kwargs.pop("creation_user_id", None) or get_random_user().id,
        text=kwargs.pop("text", None) or french_faker.paragraph(5),
        newsarticle_id=kwargs.pop("newsarticle_id", sample_news().id),
        **kwargs,
    )

    return comment


# DONNÉES DE TRANSFERT AUTO-GÉNÉRÉES

def sample_user_create_payload(username=None, realname=None, email=None, password=None, birthdate=None):
    payload = {
        "username": lorem.get_word(2) if username is None else username,
        "realname": lorem.get_word(2) if realname is None else realname,
        "email": (lorem.get_word() + "@" + lorem.get_word() + ".fr") if email is None else email,
        "password": "MotDePasse123" if password is None else password,
        "birthdate": birthdate or random_date(),
    }

    return payload


def sample_user_edit_payload(realname=None, email=None, password=None, birthdate=None, age_consent=True, bio=None,
                             sex=1):
    payload = {
        "realname": lorem.get_word(2) if realname is None else realname,
        "email": (lorem.get_word() + "@" + lorem.get_word() + ".fr") if email is None else email,
        "password": "NouveauMDP123" if password is None else password,
        "birthdate": birthdate or random_date(),
        "age_consent": age_consent,
        "bio": bio or lorem.get_paragraph(),
        "sex": sex,
    }

    return payload


def random_valid_feature_id_list():
    characteristics_id_list = []

    for characteristic_type in CharacteristicType.objects.all():
        choices = random.sample(list(characteristic_type.characteristics.values_list("pk", flat=True)), characteristic_type.min_limit)
        characteristics_id_list.extend(choices)

    return characteristics_id_list


def sample_fiction_create_payload(title=None, storynote=None, summary=None, characteristics=None, text=None):

    fiction_create_payload = {
        "title": title or lorem.get_sentence(),
        "storynote": storynote or lorem.get_sentence(),
        "summary": summary or lorem.get_sentence(),
        "characteristics": characteristics or random_valid_feature_id_list(),
        "text": text or lorem.get_paragraph(2),
    }

    return fiction_create_payload
