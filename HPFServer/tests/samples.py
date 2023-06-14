import faker

from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.utils import timezone

from core.utils import get_moderation_account
from users.models import User
from characteristics.models import Characteristic, CharacteristicType
from fictions.models import Fiction, Chapter, Collection, ChapterValidationStage
from reviews.models import FictionReview, ChapterReview, CollectionReview
from news.models import NewsArticle, NewsComment, NewsStatus


french_faker = faker.Faker("fr_FR")


def random_characteristic_type():
    characteristic_types = CharacteristicType.objects.all()
    if characteristic_types.count() > 0:
        return french_faker.random_element(characteristic_types)
    else:
        return sample_characteristic_type()


def get_random_user():
    return User.objects.exclude(pk__lte=0).order_by("?").first()


# MODÈLES AUTO-GÉNÉRÉS

def sample_user(**kwargs):
    def sample_profile_picture():
        from drf_extra_fields.fields import Base64ImageField
        import base64

        img_bytes = french_faker.image(size=(96,96))
        img_base64 = base64.encodebytes(img_bytes)
        img_base64_str = img_base64.decode("utf-8")

        return {
            "src_path": Base64ImageField().to_internal_value(img_base64_str),
        }

    def sample_profile():
        return {
            "bio": french_faker.paragraph(3),
            "gender": french_faker.random_int(min=0, max=3),
            "birthdate": french_faker.date_of_birth(),
            "realname": french_faker.name(),
            "website": french_faker.url(),
            "profile_picture": sample_profile_picture(),
        }

    user = User.objects.create_user(
        username=kwargs.pop("username", None) or french_faker.user_name(),
        email=kwargs.pop("email", None) or french_faker.email(safe=True),
        password=kwargs.pop("password", None) or make_password(None),  # mot de passe inutilisable
        profile=kwargs.pop("profile", None) or sample_profile(),
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
        fiction.last_update_date = fiction.modification_date
        fiction.save()

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
                creation_user_id=chapter.creation_user_id,
                text=french_faker.paragraph(100),
                touch=False,
            )
    return fiction


def sample_chapter(**kwargs):
    creation_user_id = kwargs.pop("creation_user_id", None) or getattr(sample_user(), "id")
    text = kwargs.pop("text", None)
    chapter = Chapter.objects.create(
        creation_user_id=creation_user_id,
        fiction_id=kwargs.pop("fiction_id", None) or getattr(sample_fiction(creation_user_id), "id"),
        title=kwargs.pop("title", None) or french_faker.sentence(),
        validation_status=kwargs.pop("validation_status", ChapterValidationStage.PUBLISHED),
        **kwargs,
    )
    chapter.create_text_version(
        creation_user_id=creation_user_id,
        text=text or french_faker.paragraph(3),
        touch=False,
    )

    return chapter

"""
def sample_collection(creation_user=None, title=None, summary=None,
                      **extra_fields):
    creation_user = creation_user or sample_user()
    collection = Collection.objects.create(
        creation_user=creation_user,
        title=lorem.get_sentence() if title is None else title,
        summary=lorem.get_paragraph() if summary is None else summary,
        **extra_fields
    )

    return collection
"""


def sample_characteristic_type(**kwargs):
    min_limit = kwargs.pop("min_limit", None)
    max_limit = kwargs.pop("max_limit", None)
    if not min_limit or max_limit:
        min_limit, max_limit = sorted(french_faker.random_elements(length=2, unique=True, elements=range(10)))
    elif min_limit:
        max_limit = french_faker.random_int(min_limit, 10)
    elif max_limit:
        min_limit = french_faker.random_int(0, max_limit)

    characteristic_type = CharacteristicType.objects.create(
        creation_user_id=kwargs.pop("creation_user_id", None) or getattr(get_moderation_account(), "id"),
        name=kwargs.pop("name", None) or french_faker.word().capitalize(),
        min_limit=min_limit,
        max_limit=max_limit,
        is_closed=kwargs.pop("is_closed", False),
        **kwargs,
    )
    return characteristic_type


def sample_characteristic(**kwargs):
    characteristic = Characteristic.objects.create(
        creation_user_id=kwargs.pop("creation_user_id", None) or getattr(get_moderation_account(), "id"),
        characteristic_type_id=kwargs.pop("characteristic_type_id", None) or getattr(random_characteristic_type(), "id"),
        name=kwargs.pop("name", None) or french_faker.word().capitalize(),
        **kwargs,
    )
    return characteristic


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
        creation_user_id=kwargs.pop("creation_user_id", None) or getattr(get_random_user(), "id"),
        text=kwargs.pop("text", None) or french_faker.paragraph(5),
        newsarticle_id=kwargs.pop("newsarticle_id", None) or getattr(sample_news(), "id"),
        **kwargs,
    )

    return comment

"""
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
"""