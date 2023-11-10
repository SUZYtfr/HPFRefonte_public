from django.test import TestCase, Client, override_settings
from core.management.utils.samples import (
    sample_user,
    sample_news,
    sample_fiction,
    sample_chapter,
    sample_fiction_review,
    get_random_characteristic_type,
)
from users.models import User
from news.models import NewsArticle, NewsComment
from news.enums import NewsCategory, NewsStatus
from fictions.models import Chapter, Fiction, Collection
from fictions.enums import ChapterValidationStage, FictionStatus, CollectionAccess
from characteristics.models import CharacteristicType, Characteristic
from reviews.models import BaseReview, FictionReview

"""
Teste le bon fonctionnement de la plate-forme d'administration

Le défaut principal de la plate-forme d'administration est qu'elle n'utilise pas le manager
des objets pour les créer : il faut la modifier pour assurer une logique similaire. Ça double
le code inutilement et c'est une source d'erreurs. 

FIXME: tests trop répétitifs et pas très stables
- On teste systématiquement la création, la modification et la récupération (liste, détail) des
objets, notamment les informations de créateur et modificateur assignés à l'utilisateur authentifié.
C'est redondant.
- La réponse du client est peu claire : HTTP 302 FOUND (pourquoi ?), et quand on suit la chaîne de
redirection : HTTP 200 OK même en cas de rejet du formulaire, puisque la réponse est une page HTML.
Il est difficile de faire des tests sur ces bases.
- Pour s'assurer que l'objet a bien été créé, par exemple, puisqu'on ne peut pas savoir son id par
la réponse, on le récupère par le manager avec .last(). Cela pose plusieurs problèmes:
- L'ordonnation de .last() peut être modifié dans le Meta de l'objet. En faisant confiance aveuglément
à .last() sans rétablir l'ordonnation par id dans les tests, on peut récupérer le mauvais objet et
fausser le résultat des tests par faux négatifs.
- Similairement, si l'objet n'est pas créé, on risque de récupérer un mauvais objet, et de faire des
tests (de créateur, modificateur) dessus qui peuvent donner de faux positifs.
- La plate-forme d'administration utilise un système de formulaire HTML bizarre pour les inlines.
(par exemple pour les éléments de série : "items-0-chapter", "items-0-id", etc.).
"""

@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}})
class TestAdminPages(TestCase):
    fixtures = [
        "fixtures/users.json",
        "fixtures/characteristics.json",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.another_client = Client()
        cls.admin_user = User.objects.get(username="admin")
        cls.random_superuser = User.objects.create_superuser(
            username="random superuser",
            email="randomsuperuser@example.com",
            password="1234",
        )

    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.admin_user)
        self.another_client.force_login(self.random_superuser)

    def test_news_article_admin_page(self) -> None:
        data = {
            "title": "test news article admin page",
            "content": "test content",
            "category": NewsCategory.ASSOCIATION,
            "status": NewsStatus.DRAFT,
            "authors": [self.admin_user.id],
        }
        
        # Création
        self.client.post(
            path="/admin/news/newsarticle/add/",
            data=data,
        )
        news_article = NewsArticle.objects.last()

        self.assertEqual(self.admin_user, news_article.creation_user)
        self.assertIsNone(news_article.modification_user)
        self.assertIn(self.admin_user, news_article.authors.all())

        # Modification
        self.another_client.post(
            path=f"/admin/news/newsarticle/{news_article.id}/change/",
            data=data,
        )
        news_article.refresh_from_db()

        self.assertEqual(self.admin_user, news_article.creation_user)
        self.assertEqual(self.random_superuser, news_article.modification_user)
        self.assertNotIn(self.random_superuser, news_article.authors.all())

        # Récupération
        news_article_changelist = self.client.get(
            path="/admin/news/newsarticle/",
        )
        news_article_change = self.client.get(
            path=f"/admin/news/newsarticle/{news_article.id}/change/",
        )
        self.assertEqual(200, news_article_changelist.status_code)
        self.assertEqual(200, news_article_change.status_code)

    def test_news_comment_admin_page(self) -> None:
        news_article = sample_news()
        data = {
            "newsarticle": news_article.id,
            "text": "test news comment admin page",
        }

        # Création
        self.client.post(
            path="/admin/news/newscomment/add/",
            data=data,
        )
        news_comment = NewsComment.objects.last()

        self.assertEqual(self.admin_user, news_comment.creation_user)
        self.assertIsNone(news_comment.modification_user)

        # Modification
        self.another_client.post(
            path=f"/admin/news/newscomment/{news_comment.id}/change/",
            data=data,
        )
        news_comment.refresh_from_db()

        self.assertEqual(self.admin_user, news_comment.creation_user)
        self.assertEqual(self.random_superuser, news_comment.modification_user)

        # Récupération
        news_comment_changelist = self.client.get(
            path="/admin/news/newscomment/",
        )
        news_comment_change = self.client.get(
            path=f"/admin/news/newscomment/{news_comment.id}/change/",
        )
        self.assertEqual(200, news_comment_changelist.status_code)
        self.assertEqual(200, news_comment_change.status_code)

    def test_chapter_admin_page(self) -> None:
        fiction = sample_fiction(chapter_count=1)
        original_text = "original text"
        data = {
            "fiction": fiction.id,
            "title": "test chapter admin page",
            "text": original_text,
            "validation_status": ChapterValidationStage.PUBLISHED,
            "read_count": 12,
        }

        # Création
        self.client.post(
            path="/admin/fictions/chapter/add/",
            data=data,
        )
        chapter = Chapter.objects.last()

        self.assertEqual(self.admin_user, chapter.creation_user)
        self.assertIsNone(chapter.modification_user)
        self.assertEqual(original_text, chapter.versions.last().text)

        # Modification
        modified_text = "modified text"
        data["text"] = modified_text
        data["fiction"] = ""
        self.another_client.post(
            path=f"/admin/fictions/chapter/{chapter.id}/change/",
            data=data,
        )
        chapter.refresh_from_db()

        self.assertEqual(self.admin_user, chapter.creation_user)
        self.assertEqual(self.random_superuser, chapter.modification_user)
        self.assertEqual(modified_text, chapter.versions.last().text)  # TODO - latest
        self.assertEqual(original_text, chapter.versions.first().text)

        # Récupération
        chapter_changelist = self.client.get(
            path="/admin/fictions/chapter/",
        )
        chapter_change = self.client.get(
            path=f"/admin/fictions/chapter/{chapter.id}/change/",
        )
        self.assertEqual(200, chapter_changelist.status_code)
        self.assertEqual(200, chapter_change.status_code)

    def test_fiction_admin_page(self) -> None:
        characteristic = Characteristic.objects.order_by("?").first()
        data = {
            "title": "test fiction admin page",
            "status": FictionStatus.PAUSED,
            "characteristics": [characteristic.id],
        }
        
        # Création
        self.client.post(
            path="/admin/fictions/fiction/add/",
            data=data,
        )
        fiction = Fiction.objects.last()

        self.assertEqual(self.admin_user, fiction.creation_user)
        self.assertIsNone(fiction.modification_user)
        self.assertIn(characteristic, fiction.characteristics.all())

        # Modification
        self.another_client.post(
            path=f"/admin/fictions/fiction/{fiction.id}/change/",
            data=data,
        )
        fiction.refresh_from_db()

        self.assertEqual(self.admin_user, fiction.creation_user)
        self.assertEqual(self.random_superuser, fiction.modification_user)

        # Récupération
        fiction_changelist = self.client.get(
            path="/admin/fictions/fiction/",
        )
        fiction_change = self.client.get(
            path=f"/admin/fictions/fiction/{fiction.id}/change/",
        )
        self.assertEqual(200, fiction_changelist.status_code)
        self.assertEqual(200, fiction_change.status_code)

    """
    def test_collection_admin_page(self) -> None:
        # TODO - trouver un moyen de tester les inlines
    """

    def test_characteristic_type_admin_page(self):
        data = {
            "name": "test characteristic type admin page",
            "min_limit": 2,
            "is_closed": False,
        }
        
        # Création
        self.client.post(
            path="/admin/characteristics/characteristictype/add/",
            data=data,
        )
        characteristic_type = CharacteristicType.objects.last()

        self.assertEqual(self.admin_user, characteristic_type.creation_user)
        self.assertIsNone(characteristic_type.modification_user)

        # Modification
        self.another_client.post(
            path=f"/admin/characteristics/characteristictype/{characteristic_type.id}/change/",
            data=data,
        )
        characteristic_type.refresh_from_db()

        self.assertEqual(self.admin_user, characteristic_type.creation_user)
        self.assertEqual(self.random_superuser, characteristic_type.modification_user)

        # Récupération
        characteristic_type_changelist = self.client.get(
            path="/admin/characteristics/characteristictype/",
        )
        characteristic_type_change = self.client.get(
            path=f"/admin/characteristics/characteristictype/{characteristic_type.id}/change/",
        )
        self.assertEqual(200, characteristic_type_changelist.status_code)
        self.assertEqual(200, characteristic_type_change.status_code)

    def test_characteristic_admin_page(self):
        characteristic_type = get_random_characteristic_type()
        data = {
            "name": "test characteristic admin page",
            "characteristic_type": characteristic_type.id,
        }
        
        # Création
        self.client.post(
            path="/admin/characteristics/characteristic/add/",
            data=data,
        )
        characteristic = Characteristic.objects.order_by("id").last()

        self.assertEqual(self.admin_user, characteristic.creation_user)
        self.assertIsNone(characteristic.modification_user)

        # Modification
        self.another_client.post(
            path=f"/admin/characteristics/characteristic/{characteristic.id}/change/",
            data=data,
        )
        characteristic.refresh_from_db()

        self.assertEqual(self.admin_user, characteristic.creation_user)
        self.assertEqual(self.random_superuser, characteristic.modification_user)

        # Récupération
        characteristic_changelist = self.client.get(
            path="/admin/characteristics/characteristic/",
        )
        characteristic_change = self.client.get(
            path=f"/admin/characteristics/characteristic/{characteristic.id}/change/",
        )
        self.assertEqual(200, characteristic_changelist.status_code)
        self.assertEqual(200, characteristic_change.status_code)

    def test_fiction_review_admin_page(self):
        fiction = sample_fiction(chapter_count=1)

        test_text = "test fiction review admin page"
        data = {
            "fiction": fiction.id,
            "text": test_text,
            "grading": 6,
            "is_draft": False,
        }
        
        # Création
        self.client.post(
            path="/admin/reviews/fictionreview/add/",
            data=data,
        )
        fiction_review = FictionReview.objects.last()

        self.assertEqual(self.admin_user, fiction_review.creation_user)
        self.assertIsNone(fiction_review.modification_user)
        self.assertEqual(test_text, fiction_review.text)

        # Modification
        self.another_client.post(
            path=f"/admin/reviews/fictionreview/{fiction_review.id}/change/",
            data=data,
        )
        fiction_review.refresh_from_db()

        self.assertEqual(self.admin_user, fiction_review.creation_user)
        self.assertEqual(self.random_superuser, fiction_review.modification_user)

        # Récupération
        fiction_review_changelist = self.client.get(
            path="/admin/reviews/fictionreview/",
        )
        fiction_review_change = self.client.get(
            path=f"/admin/reviews/fictionreview/{fiction_review.id}/change/",
        )
        self.assertEqual(200, fiction_review_changelist.status_code)
        self.assertEqual(200, fiction_review_change.status_code)

    def test_review_reply_admin_page(self):
        fiction_review = sample_fiction_review()

        test_text = "test fiction review admin page"
        data = {
            "parent": fiction_review.id,
            "text": test_text,
            "is_draft": False,
        }
        
        # Création
        self.client.post(
            path="/admin/reviews/basereview/add/",
            data=data,
        )
        review_reply = BaseReview.objects.last()

        self.assertEqual(self.admin_user, review_reply.creation_user)
        self.assertIsNone(review_reply.modification_user)
        self.assertEqual(test_text, review_reply.text)

        # Modification
        self.another_client.post(
            path=f"/admin/reviews/basereview/{review_reply.id}/change/",
            data=data,
        )
        review_reply.refresh_from_db()

        self.assertEqual(self.admin_user, review_reply.creation_user)
        self.assertEqual(self.random_superuser, review_reply.modification_user)

        # Récupération
        review_reply_changelist = self.client.get(
            path="/admin/reviews/basereview/",
        )
        review_reply_change = self.client.get(
            path=f"/admin/reviews/basereview/{review_reply.id}/change/",
        )
        self.assertEqual(200, review_reply_changelist.status_code)
        self.assertEqual(200, review_reply_change.status_code)


    """
    # TODO - trouver un moyen de tester les inlines
    def test_user_admin_page(self):
        self.fail()
    """
        