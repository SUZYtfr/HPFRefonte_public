from users.models import User as UserModel
from features.models import Feature as FeatureModel, Category as CategoryModel
from fictions.models import Fiction as FictionModel, Chapter as ChapterModel
from colls.models import Collection as CollectionModel
from reviews.models import Review as ReviewModel
from polls.models import PollGroup as PollGroupModel, PollQuestion as PollQuestionModel, PollAnswer as PollAnswerModel
from news.models import NewsArticle as NewsArticleModel, NewsComment

# Trouver mieux que lorem, malheureusement django-autofixture n'est plus compatible
# Lorem risque de donner deux fois le même nickname par exemple...
import lorem
import time
import datetime
import random

from django.conf import settings


def random_category():
    if CategoryModel.objects.count() > 0:
        return random.choices(list(CategoryModel.objects.all()))[0]
    else:
        return sample_category()


def random_date():
    d = random.randint(1, int(time.time()))
    return datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d')


# MODÈLES AUTO-GÉNÉRÉS

def sample_user(nickname=None, email=None, password=None, birthdate=None,
                **extra_fields):
    user = UserModel.objects.create_user(
        nickname=nickname or lorem.get_word(2),
        email=email or lorem.get_word() + "@" + lorem.get_word() + ".fr",
        password=password or "MotDePasse123",
        birthdate=birthdate or random_date(),
        **extra_fields
    )

    return user


def sample_chapter():
    pass


def sample_fiction(creation_user=None, title=None, generate_chapters=0, **extra_fields):
    fiction = FictionModel.objects.create(
        creation_user=creation_user or sample_user(),
        title=lorem.get_sentence() if title is None else title,
        **extra_fields
    )

    [sample_chapter(creation_user=creation_user, fiction=fiction) for x in range(generate_chapters)]

    return fiction


def sample_chapter(creation_user=None, title=None, fiction=None, text=None,
                   **extra_fields):
    if not creation_user:
        creation_user = sample_user()
    if not fiction:
        fiction = sample_fiction(creation_user=creation_user)
    chapter = ChapterModel.objects.create(
        creation_user=creation_user,
        title=lorem.get_sentence() if title is None else title,
        fiction=fiction,
        text=text or lorem.get_paragraph(3),
        **extra_fields
    )

    return chapter


def sample_collection(creation_user=None, title=None, summary=None,
                      **extra_fields):
    creation_user = creation_user or sample_user()
    collection = CollectionModel.objects.create(
        creation_user=creation_user,
        title=lorem.get_sentence() if title is None else title,
        summary=lorem.get_paragraph() if summary is None else summary,
        # starting_chapters=[sample_chapter(creation_user=creation_user)] if starting_chapters is None else starting_chapters,
        **extra_fields
    )

    return collection


def sample_category(creation_user=None, name=None, min_limit=None, max_limit=None, is_closed=False, **extra_fields):
    if not min_limit or max_limit:
        min_limit, max_limit = sorted(random.choices(range(0, 10), k=2))
    elif min_limit:
        max_limit = random.randint(min_limit, 10)
    elif max_limit:
        min_limit = random.randint(0, max_limit)

    category = CategoryModel.objects.create(
        creation_user=creation_user or UserModel.objects.get(pk=settings.MODERATION_ACCOUNT_ID),
        name=lorem.get_word(3) if name is None else name,
        min_limit=min_limit,
        max_limit=max_limit,
        is_closed=is_closed,
        **extra_fields,
    )
    return category


def sample_feature(category=None, creation_user=None, name=None,
                   **extra_fields):
    feature = FeatureModel.objects.create(
        creation_user=creation_user or UserModel.objects.get(pk=settings.MODERATION_ACCOUNT_ID),
        category=category or sample_category(),
        name=lorem.get_word(3) if name is None else name,
        **extra_fields
    )
    return feature


def sample_review(creation_user=None, content=None, work=None, object_type=None, text=None,
                  **extra_fields):
    types_to_models = {"fiction": sample_fiction,
                       "chapter": sample_chapter,
                       "collection": sample_collection,
                       "author": sample_user}

    if not work:
        work = types_to_models.get(object_type or "fiction")()

    return ReviewModel.objects.create(
        creation_user=creation_user or sample_user(),
        content=lorem.get_paragraph() if content is None else content,
        work=work,
        text=text or lorem.get_paragraph(2),
        **extra_fields
    )


def sample_poll_group(**kwargs):
    poll_group = PollGroupModel.objects.create(
        creation_user=kwargs.pop("creation_user", sample_user()),
        title=kwargs.pop("title", lorem.get_word(count=5)),
        **kwargs
    )

    return poll_group


def sample_poll_question(**kwargs):
    poll_group = kwargs.get("poll_group", None)

    poll_question = PollQuestionModel.objects.create(
        creation_user=kwargs.pop("creation_user", getattr(poll_group, "creation_user", sample_user())),
        question_text=kwargs.pop("question_text", lorem.get_sentence()),
        **kwargs,
    )

    return poll_question


def sample_poll_answer(**kwargs):
    poll_question = kwargs.pop("poll_question", sample_poll_question())

    poll_answer = PollAnswerModel.objects.create(
        poll_question=poll_question,
        creation_user=kwargs.pop("creation_user", poll_question.creation_user),
        answer_text=kwargs.pop("answer_text", lorem.get_sentence()),
    )

    return poll_answer


def sample_news(**kwargs):
    status = kwargs.pop("status", None)

    news = NewsArticleModel.objects.create(
        creation_user=kwargs.pop("creation_user", sample_user()),
        title=kwargs.pop("title", lorem.get_sentence()),
        content=kwargs.pop("content", lorem.get_paragraph()),
        category=kwargs.pop("category", NewsArticleModel.NewsCategory.UNDEFINED),
        status=status,
        **kwargs,
    )

    if status == NewsArticleModel.NewsStatus.PUBLISHED:
        news.post(modification_user=news.creation_user)

    return news


def sample_comment(**kwargs):
    comment = NewsComment.objects.create(
        creation_user=kwargs.pop("creation_user", sample_user()),
        text=kwargs.pop("text", lorem.get_paragraph()),
        newsarticle=kwargs.pop("newsarticle", sample_news()),
        **kwargs,
    )

    return comment


# DONNÉES DE TRANSFERT AUTO-GÉNÉRÉES

def sample_user_create_payload(nickname=None, realname=None, email=None, password=None, birthdate=None):
    payload = {
        "nickname": lorem.get_word(2) if nickname is None else nickname,
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
    features_id_list = []

    for category in CategoryModel.objects.all():
        choices = random.sample(list(category.features.values_list("pk", flat=True)), category.min_limit)
        features_id_list.extend(choices)

    return features_id_list


def sample_fiction_create_payload(title=None, storynote=None, summary=None, features=None, text=None):

    fiction_create_payload = {
        "title": title or lorem.get_sentence(),
        "storynote": storynote or lorem.get_sentence(),
        "summary": summary or lorem.get_sentence(),
        "features": features or random_valid_feature_id_list(),
        "text": text or lorem.get_paragraph(2),
    }

    return fiction_create_payload
