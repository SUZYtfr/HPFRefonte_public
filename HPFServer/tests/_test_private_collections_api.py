from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.test import APIClient, APITestCase, APIRequestFactory

from colls.serializers import MyCollectionSerializer, MyCollectionCardSerializer

from tests.samples import *

MY_COLLECTION_URL = reverse("app:mycollections:mycollection-list")


def generate_mycollection_detail_url(collection_id):
    return reverse("app:mycollections:mycollection-detail", args=[collection_id])


class TestsMyCollectionsAPI(APITestCase):
    """Testent le comportement de l'API privée des séries"""

    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")
        cls.client = APIClient()
        cls.author = sample_user()

    def setUp(self) -> None:
        self.client.force_authenticate(self.author)

    def test_user_can_retrieve_collection_list(self):
        """"Teste qu'un utilisateur authentifié peut récupérer la liste de ses séries"""
        [sample_collection(creation_user=self.author) for x in range(3)]
        collection_cards_serializer = MyCollectionCardSerializer(self.author.collections.all(),
                                                                 many=True,
                                                                 context={"request": self.request})

        res = self.client.get(MY_COLLECTION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, collection_cards_serializer.data)

    def test_user_can_retrieve_collection(self):
        """Teste qu'un utilisateur authentifié peut récupérer une de ses séries"""
        collection = sample_collection(creation_user=self.author)
        collection_serializer = MyCollectionSerializer(collection, context={"request": self.request})

        res = self.client.get(generate_mycollection_detail_url(collection.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, collection_serializer.data)

    def test_user_can_create_collection(self):
        """Teste qu'un utilisateur authentifié peut créer une nouvelle série"""
        fiction1 = sample_fiction(creation_user=self.author, generate_chapters=2)
        fiction2 = sample_fiction(creation_user=self.author, generate_chapters=2)

        # Insertion d'un chapitre isolé entre deux chapitre d'une même fiction
        starting_chapters_id = [fiction1.chapters.first().id, fiction2.chapters.last().id, fiction1.chapters.first().id]

        payload = {
            "title": "Exemple de titre de série",
            "summary": "Exemple de résumé de série",
            "status": 3,
            "chapters": starting_chapters_id
        }

        res = self.client.post(MY_COLLECTION_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["status"], payload["status"])
        self.assertEqual(res.data["summary"], payload["summary"])
        self.assertTrue(self.author.collections.get(id=res.data["id"]))
        self.assertEqual(self.author.collections.get(id=res.data["id"]).chapters.count(), 3)
        self.assertEqual(list(self.author.collections.get(id=res.data["id"]).chapters.order_by("work__order").values_list("id", flat=True)),
                         starting_chapters_id)

    def test_user_can_edit_collection(self):
        """Teste qu'un utilisateur authentifié peut modifier une de ses séries"""
        chapter1 = sample_chapter(fiction=sample_fiction(creation_user=self.author))
        collection = sample_collection(creation_user=self.author, starting_chapters=[chapter1])
        chapter2 = sample_chapter(fiction=sample_fiction(creation_user=self.author))

        payload = {
            "title": "Titre modifié",
            "summary": "Résumé modifié",
            "status": 2,
            "chapters": [chapter2.id]
        }

        res = self.client.put(generate_mycollection_detail_url(collection_id=collection.id), payload)

        collection.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(collection.title, payload["title"])
        self.assertEqual(collection.status, payload["status"])
        self.assertEqual(collection.summary, payload["summary"])
        self.assertNotIn(chapter1, collection.chapters.all())
        self.assertIn(chapter2, collection.chapters.all())

    def test_user_can_delete_collection_if_only_author(self):
        """Teste qu'un utilisateur authentifié peut supprimer une de ses collections s'il en est le seul auteur"""
        collection = sample_collection(creation_user=self.author)
        collection_id = collection.id

        res = self.client.delete(generate_mycollection_detail_url(collection_id=collection.id))
        res2 = self.client.get(generate_mycollection_detail_url(collection_id=collection_id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)
        with self.assertRaises(ObjectDoesNotExist):
            collection.refresh_from_db()

    def test_user_can_renounce_authorship_on_collection_if_many_authors(self):
        """Teste qu'un utilisateur authentifié peut se retirer de la liste des auteurs d'une collection co-authorée"""
        collection = sample_collection(creation_user=self.author)
        collection_id = collection.id
        author2 = sample_user()
        collection.authors.add(author2)

        res = self.client.delete(generate_mycollection_detail_url(collection_id=collection.id))
        res2 = self.client.get(generate_mycollection_detail_url(collection_id=collection_id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(author2.collections.get(id=collection.id))
