from django.test import TestCase, override_settings

from core.management.utils.samples import (
    sample_user,
    sample_collection,
    sample_fiction,
    sample_chapter,
    sample_news,
    sample_comment,
    format_editor_content,
)
from core.text_functions import count_words
from users.models import User
from fictions.enums import (
    CollectionAccess,
    FictionStatus,
    ChapterValidationStage,
)
from news.enums import (
    NewsCategory,
    NewsStatus,
)


"""
Teste les fonctions de génération aléatoire de ressources.
"""

@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}})
class TestSampleFunctions(TestCase):
    fixtures = [
        "fixtures/users.json",
        "fixtures/characteristics.json",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.random_user = User.objects.exclude(id__lte=0).first()
        cls.random_user_id = getattr(cls.random_user, "id")
        return super().setUpTestData()

    def test_basic_user_sample(self) -> None:
        """Un utilisateur entier est-il créé ?"""

        user = sample_user(with_profile_picture=True)
        
        self.assertIsNotNone(user.profile)
        self.assertIsNotNone(user.profile.profile_picture)
        self.assertIsNotNone(user.preferences)

    def test_advanced_user_sample(self) -> None:
        """
        Tous les détails d'un utilisateur peuvent-ils être donnés ?
        TODO - test bio images et profilepicture
        https://docs.djangoproject.com/en/4.2/ref/files/storage/#the-inmemorystorage-class
        """

        test_password = "Test1234!"
        test_birthdate = "1988-12-12"
        test_base_data = {
            "username": "test username",
            "email": "test@example.com",
        }
        test_profile_data = {
            "realname": "test realname",
            "bio": "Test bio",
            "website": "https://perdu.com",
        }

        user = sample_user(
            password=test_password,
            profile={
                "birthdate": test_birthdate,
                **test_profile_data
            },
            **test_base_data,
        )

        self.assertTrue(user.check_password(test_password))
        self.assertDictContainsSubset(test_base_data, vars(user))
        self.assertDictContainsSubset(test_profile_data, vars(user.profile))
        self.assertEqual(test_birthdate, str(user.profile.birthdate))

    def test_basic_collection_sample(self) -> None:
        collection = sample_collection()

        self.assertNotEqual(0, collection.characteristics.count())
        self.assertNotEqual(0, collection.items.count())

    def test_advanced_collection_sample(self) -> None:
        test_data = {
            "creation_user_id": self.random_user_id,
            "title": "test title",
            "summary": "test summary",
            "access": CollectionAccess.MODERATED,
        }
        
        collection = sample_collection(
            **test_data,
        )

        self.assertDictContainsSubset(test_data, vars(collection))

    def test_basic_fiction_sample(self) -> None:
        """Une fiction entière peut-elle être créée ?"""

        fiction = sample_fiction(image_count=0)

        self.assertNotEqual(0, fiction.characteristics.count())
        self.assertNotEqual(0, fiction.chapters.count())

    def test_advanced_fiction_sample(self) -> None:
        """"""
        
        test_data = {
            "creation_user_id": self.random_user_id,
            "title": "test title",
            "summary": "test summary",
            "storynote": "test storynote",
            "status": FictionStatus.COMPLETED,
            "featured": True,
        }

        fiction = sample_fiction(
            chapter_count=2,
            image_count=0,
            **test_data,
        )

        self.assertDictContainsSubset(test_data, vars(fiction))
        self.assertEqual(2, fiction.chapters.count())

    def test_basic_chapter_sample(self) -> None:
        """Un chapitre entier peut-il être créé ?"""

        chapter = sample_chapter(image_count=0)

        self.assertIsNotNone(chapter.text)
        self.assertNotEqual("", chapter.text)
        self.assertIsNotNone(chapter.word_count)
        self.assertNotEqual(0, chapter.word_count)

    def test_advanced_chapter_sample(self):
        """
        Tous les détails d'un chapitre peuvent-ils être donnés ?
        TODO - test ImageContent
        """

        test_text = "test text"
        test_data = {
            "creation_user_id": self.random_user_id,
            "title": "test title",
            "startnote": "test startnote",
            "endnote": "test endnote",
            "validation_status": ChapterValidationStage.DRAFT,
            "read_count": 1250,
        }

        chapter = sample_chapter(
            image_count=0,
            text=test_text,
            **test_data,
        )

        self.assertDictContainsSubset(test_data, vars(chapter))
        self.assertEqual(format_editor_content(test_text), chapter.text)
        self.assertEqual(count_words(test_text), chapter.word_count)

    def test_basic_news_article_sample(self):
        news_article = sample_news()

        self.assertNotEqual(0, news_article.authors.count())

    def test_advanced_news_article_sample(self):
        test_post_date = "2023-12-12T10:12:21.550Z"
        test_data = {
            "creation_user_id": self.random_user_id,
            "title": "test title",
            "content": "test content",
            "category": NewsCategory.ASSOCIATION,
            "status": NewsStatus.DRAFT,
        }

        news_article = sample_news(
            post_date=test_post_date,
            **test_data,
        )

        self.assertEqual(self.random_user_id, news_article.authors.first().id)
        self.assertEqual(test_post_date, str(news_article.post_date))
        self.assertDictContainsSubset(test_data, vars(news_article))

    def test_basic_news_comment_sample(self):
        news_comment = sample_comment()

        self.assertIsNotNone(news_comment)

    def test_advanced_news_comment_sample(self):
        news_article = sample_news()

        test_text = "test text"
        test_data = {
            "creation_user_id": self.random_user_id,
            "newsarticle_id": news_article.id,
        }
        
        news_comment = sample_comment(
            text=test_text,
            **test_data,
        )

        self.assertDictContainsSubset(test_data, vars(news_comment))
        self.assertEqual(format_editor_content(test_text), news_comment.text)

    @classmethod
    def tearDownClass(cls) -> None:
        # TODO - supprimer toutes les images de test du fichier de système
        return super().tearDownClass()
