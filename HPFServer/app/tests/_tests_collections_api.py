from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status
from tests.samples import *


def generate_coll_chapter_order_url(collection_id):
    return reverse("app:collections:collection-chapter-order", args=[collection_id])


class TestsCollectionManagement(APITestCase):
    """Testent les actions de gestion de séries"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.collection = sample_collection(creation_user=cls.author)
        [cls.collection.chapters.add(sample_chapter(creation_user=cls.author).id) for x in range(3)]
        cls.client = APIClient()

    def setUp(self) -> None:
        self.client.force_authenticate(self.author)

    def test_collection_chapter_order(self):
        """Teste que l'ordre des chapitres d'une série peut être récupéré"""

        order = list(self.collection.get_work_order().values_list("chapter_id", flat=True))

        res = self.client.get(generate_coll_chapter_order_url(self.collection.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["order"], order)

    def test_chapter_reordering(self):
        """Teste que les chapitres d'une série peuvent être réordonnés"""

        order = list(self.collection.get_work_order().values_list("chapter_id", flat=True))
        random.shuffle(order)

        res = self.client.put(generate_coll_chapter_order_url(self.collection.id), data={"order": order})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(list(self.collection.get_work_order()), order)

    def test_chapter_id_integrity_for_reordering(self):
        """Teste que les IDs passés doivent correspondre à ceux des chapitres"""

        order = list(self.collection.get_work_order().values_list("chapter_id", flat=True))

        extra_id_order = order.copy()
        extra_id_order.append(99)

        res = self.client.put(generate_coll_chapter_order_url(self.collection.id), data={"order": extra_id_order})

        missing_id_order = order.copy()
        missing_id_order.pop()

        res2 = self.client.put(generate_coll_chapter_order_url(self.collection.id), data={"order": missing_id_order})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
