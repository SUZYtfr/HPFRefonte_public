import random

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from fictions.serializers import MyFictionSerializer, MyFictionCardSerializer

from tests.samples import *

from fictions.models import Fiction, Chapter


def generate_myfiction_url(fiction_id=None):
    if fiction_id:
        return reverse("app:myfictions:myfiction-detail", args=[fiction_id])
    else:
        return reverse("app:myfictions:myfiction-list")


class TestsMyFictionsAPI(APITestCase):
    """Testent le comportement de l'API privée des fictions"""

    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")
        cls.client = APIClient()
        cls.author = sample_user()
        # Fiction non-publiée
        cls.unpublished_fiction = sample_fiction(creation_user=cls.author)
        cls.unvalidated_chapter = sample_chapter(creation_user=cls.author, fiction=cls.unpublished_fiction)

        # Fiction publiée
        cls.published_fiction = sample_fiction(creation_user=cls.author)
        cls.validated_chapter = sample_chapter(creation_user=cls.author, fiction=cls.published_fiction,
                                               validation_status=Chapter.ValidationStage.PUBLISHED)

        # Crée une liste d'ID dont le nombre correspond au minimum pour chaque catégorie de caractéristique
        cls.features_id_list = [sample_characteristic(creation_user=category.creation_user, characteristic_type=category).id
                                for category in CATEGORIES.values()
                                for x in range(category.min_limit)]

    def setUp(self) -> None:
        self.client.force_authenticate(self.author)

    def test_user_can_retrieve_fiction_list(self):
        """"Teste qu'un utilisateur authentifié peut récupérer la liste de ses fictions"""
        fiction_cards_serializer = MyFictionCardSerializer(self.author.fictions.all(),
                                                           many=True,
                                                           context={"request": self.request})
        unpublished_fiction_card_serializer = MyFictionCardSerializer(self.unpublished_fiction,
                                                                      context={"request": self.request})

        res = self.client.get(generate_myfiction_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, fiction_cards_serializer.data)
        self.assertIn(unpublished_fiction_card_serializer.data, fiction_cards_serializer.data)

    def test_user_can_retrieve_fiction(self):
        """Teste qu'un utilisateur authentifié peut récupérer une de ses fictions"""
        fiction_serializer = MyFictionSerializer(self.published_fiction, context={"request": self.request})

        res = self.client.get(generate_myfiction_url(self.published_fiction.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, fiction_serializer.data)

    def test_user_can_create_fiction(self):
        """Teste qu'un utilisateur authentifié peut créer une nouvelle fiction"""

        payload = {
            "title": "Exemple de titre de fiction",
            "storynote": "Exemple de note de fiction",
            "summary": "Exemple de résumé",
            "features": self.features_id_list,
        }

        res = self.client.post(generate_myfiction_url(), payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.author.fictions.filter(id=res.data["id"]).exists())

    def test_user_can_edit_fiction(self):
        """Teste qu'un utilisateur authentifié peut modifier une de ses fictions"""
        fiction = sample_fiction(creation_user=self.author, chapter_count=1)

        payload = {
            "title": "Titre modifié",
            "storynote": "Note de fiction modifié",
            "summary": "Résumé modifié",
        }

        res = self.client.patch(generate_myfiction_url(fiction.id), payload)

        fiction.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(fiction.title, payload["title"])
        self.assertEqual(fiction.storynote, payload["storynote"])
        self.assertEqual(fiction.summary, payload["summary"])

    def test_user_can_delete_fiction_if_only_author(self):
        """Teste qu'un utilisateur authentifié peut supprimer une de ses fictions s'il en est le seul auteur"""
        fiction = sample_fiction(creation_user=self.author)

        res = self.client.delete(generate_myfiction_url(fiction_id=fiction.id))
        res2 = self.client.get(generate_myfiction_url(fiction_id=fiction.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(Fiction.DoesNotExist):
            Fiction.objects.get(pk=fiction.id)

    def test_user_can_renounce_authorship_on_fiction_if_many_authors(self):
        """Teste qu'un utilisateur authentifié peut se retirer de la liste des auteurs d'une fiction co-authorée"""
        fiction = sample_fiction(creation_user=self.author)
        author2 = sample_user()
        fiction.authors.add(author2)

        res = self.client.delete(generate_myfiction_url(fiction_id=fiction.id))
        res2 = self.client.get(generate_myfiction_url(fiction_id=fiction.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(author2.fictions.get(id=fiction.id))

    @classmethod
    def tearDownClass(cls):
        cls.author.delete()


def generate_myfiction_chapter_order_url(fiction_id):
    return reverse("app:myfictions:myfiction-chapter-order", args=[fiction_id])


class TestsFictionChapterOrdering(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.fiction = sample_fiction(creation_user=cls.author, chapter_count=4)
        cls.client = APIClient()

    def setUp(self) -> None:
        self.client.force_authenticate(self.author)

    def test_chapter_order(self):
        res = self.client.get(generate_myfiction_chapter_order_url(self.fiction.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["order"], list(self.fiction.get_chapter_order()))

    def test_chapter_reordering(self):
        order = list(self.fiction.get_chapter_order())
        random.shuffle(order)

        res = self.client.put(generate_myfiction_chapter_order_url(self.fiction.id), data={"order": order})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(list(self.fiction.get_chapter_order()), order)

    def test_chapter_id_integrity_for_reordering(self):
        order = list(self.fiction.get_chapter_order())

        extra_id_order = order.copy()
        extra_id_order.append(99)

        res = self.client.put(generate_myfiction_chapter_order_url(self.fiction.id), data={"order": extra_id_order})

        missing_id_order = order.copy()
        missing_id_order.pop()

        res2 = self.client.put(generate_myfiction_chapter_order_url(self.fiction.id), data={"order": missing_id_order})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
