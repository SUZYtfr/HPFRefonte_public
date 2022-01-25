from django.urls import reverse

from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from rest_framework import status

from fictions.models import Chapter
from fictions.serializers import MyChapterCardSerializer, MyChapterSerializer

from tests.samples import *


def generate_mychapter_url(chapter_id=None, fiction_id=None):
    if chapter_id:
        return reverse("app:mychapters:mychapter-detail", args=[chapter_id])
    elif fiction_id:
        return reverse("app:myfictions:myfiction-chapter-list", args=[fiction_id])
    else:
        return reverse("app:mychapters:mychapter-list")


def generate_mychapter_validate_url(chapter_id):
    return reverse("app:mychapters:mychapter-submit", args=[chapter_id])


class TestsMyChaptersAPI(APITestCase):
    """Testent le comportement de l'API privée de gestion de chapitres"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")
        cls.author = sample_user()

    def setUp(self) -> None:
        self.client.force_authenticate(self.author)

    def test_user_can_create_new_chapter(self):
        """Teste qu'un utilisateur authentifié peut créer un nouveau chapitre pour sa fiction"""
        fiction = sample_fiction(creation_user=self.author, generate_chapters=0)
        payload = {
            "title": "Exemple de titre de chapitre",
            "startnote": "Exemple de note de fiction",
            "endnote": "Exemple de résumé",
            "text": "Exemple de texte de chapitre"
        }

        res = self.client.post(generate_mychapter_url(fiction_id=fiction.id), payload)

        fiction.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.author.chapters.get(id=res.data["id"]))
        self.assertEqual(fiction.chapters.first().id, res.data["id"])

    def test_user_can_retrieve_chapter(self):
        """Teste qu'un utilisateur authentifié peut récupérer les informations d'un chapitre de sa fiction"""
        chapter = sample_chapter(creation_user=self.author)
        chapter_serializer = MyChapterSerializer(chapter, context={"request": self.request})

        res = self.client.get(generate_mychapter_url(chapter.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, chapter_serializer.data)

    def test_user_can_edit_chapter(self):
        """Teste qu'un utilisateur authentifié peut modifier les informations d'un chapitre de sa fiction"""
        chapter = sample_chapter(creation_user=self.author)
        payload = {
            "title": "Titre modifié",
            "startnote": "Note de début modifiée",
            "endnote": "Note de fin modifiée",
            "text": "Texte de chapitre modifié",
        }

        res = self.client.put(generate_mychapter_url(chapter.id), payload)

        chapter.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(chapter.title, payload["title"])
        self.assertEqual(chapter.startnote, payload["startnote"])
        self.assertEqual(chapter.endnote, payload["endnote"])

    def test_user_can_delete_chapter_if_only_author(self):
        """Teste qu'un utilisateur authentifié peut supprimer un chapitre dont il est l'unique auteur"""
        chapter = sample_chapter(creation_user=self.author)

        res = self.client.delete(generate_mychapter_url(chapter.id))
        res2 = self.client.get(generate_mychapter_url(chapter.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(Chapter.DoesNotExist):
            Chapter.objects.get(pk=chapter.id)

    # TODO - Ceci pose problème, à quelle fiction appartient alors ce chapitre ?
    # def test_user_can_renounce_authorship_on_chapter_if_any_authors(self):
    #     """Teste qu'un utilisateur authentifié peut se retirer de la liste des auteurs d'un chapitre co-autoré"""
    #     self.assertTrue(False)


class TestsChapterValidation(APITestCase):
    """Testent la validation de chapitre"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user(is_premium=False)
        cls.fiction = sample_fiction(creation_user=cls.author)
        cls.chapter = sample_chapter(creation_user=cls.author, fiction=cls.fiction)

        cls.client = APIClient()

    def setUp(self) -> None:
        self.author.is_premium = False
        self.author.save()

        self.chapter.validation_status = Chapter.ChapterValidationStage.DRAFT
        self.chapter.save()

        self.client.force_authenticate(self.author)

    def test_user_can_send_chapter_to_validation(self):
        """Teste qu'un utilisateur peut envoyer son chapitre pour validation"""

        res = self.client.put(generate_mychapter_validate_url(self.chapter.id))

        self.chapter.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.chapter.validation_status, Chapter.ChapterValidationStage.PENDING)

    def test_premium_member_skips_validation(self):
        """Teste qu'un adhérent publie automatiquement son chapitre"""

        self.author.is_premium = True
        self.author.save()

        res = self.client.put(generate_mychapter_validate_url(self.chapter.id))

        self.chapter.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.chapter.validation_status, Chapter.ChapterValidationStage.PUBLISHED)

    def test_chapter_validation_while_beta_ongoing_fails(self):
        """Teste que la validation ne peut pas être demandée si le chapitre est en cours de bêtatage"""

        self.chapter.validation_status = Chapter.ChapterValidationStage.BETA_ONGOING
        self.chapter.save()

        res = self.client.put(generate_mychapter_validate_url(self.chapter.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_mess_with_request(self):
        """Teste plusieurs scénarios de manipulation d'URL ou de requêtes HTML"""

        random_fiction = sample_fiction()
        random_chapter = sample_chapter(validation_status=Chapter.ChapterValidationStage.DRAFT, fiction=random_fiction)

        res = self.client.put(generate_mychapter_validate_url(random_chapter.id))
        random_chapter.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(random_chapter.validation_status, Chapter.ChapterValidationStage.DRAFT)

    def tearDown(self) -> None:
        self.author.fictions.clear()

    @classmethod
    def tearDownClass(cls):
        cls.author.delete()
