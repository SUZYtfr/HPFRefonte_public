from django.urls import reverse

from rest_framework.test import APITestCase, APIClient, APIRequestFactory

from rest_framework import status
from colls.models import Collection
from colls.serializers import CollectionCardSerializer, CollectionSerializer

from tests.samples import *

COLLECTION_LIST_URL = reverse("app:collections:collection-list")


def generate_collection_detail_url(collection_id):
    return reverse("app:collections:collection-detail", args=[collection_id])


class Tests_FictionsAPI(APITestCase):
    """Testent le comportement public de l'API de fictions"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        # Ceci permet d'inclure le contexte pour le test sur les sérialiseurs de liens
        # cf: https://stackoverflow.com/questions/34438290/assertionerror-hyperlinkedidentityfield-requires-the-request-in-the-serialize
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get('/')

    def test_collection_list_returns_correct_data(self):
        """Teste que la page de listage de séries renvoie les informations correctes"""
        [sample_collection() for x in range(3)]
        collection_list = Collection.objects.all()
        collection_list_serializer = CollectionCardSerializer(collection_list, many=True,
                                                              context={"request": self.request})

        res = self.client.get(path=COLLECTION_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, collection_list_serializer.data)

    def test_collection_detail_returns_correct_data(self):
        """Teste que la page de détail d'une série renvoie les informations correctes"""
        collection = sample_collection()
        collection_serializer = CollectionSerializer(collection, context={"request": self.request})

        res = self.client.get(path=generate_collection_detail_url(collection_id=collection.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, collection_serializer.data)
