from rest_framework.test import APITestCase, override_settings
from rest_framework.reverse import reverse
from rest_framework import status

from core.management.utils.samples import (
    sample_user,
    sample_fiction,
    get_random_characteristic_type,
    get_random_characteristic,
)

from users.models import User

"""
TODO
users API
reviews API
news API
images API
"""

@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}})
class TestAccountAPI(APITestCase):
    def test_account_api(self):
        username = "test account api"
        password = "password1234"
        data = {
            "email": "test-api@example.com",
        }
        
        # CRÉATION
        user_create_response = self.client.post(
            path=reverse("account:current_user"),
            data={
                **data,
                "password": password,
                "username": username,
            },
        )

        self.assertContains(user_create_response, "profile", status_code=status.HTTP_201_CREATED)
        self.assertContains(user_create_response, "preferences", status_code=status.HTTP_201_CREATED)
        self.assertNotContains(user_create_response, "password", status_code=status.HTTP_201_CREATED)

        user = User.objects.get(id=user_create_response.json()["id"])
        self.assertTrue(user.check_password(password))

        # JETONS
        get_access_token_response = self.client.post(
            path=reverse("account:token_obtain_pair"),
            data={
                "username": username,
                "password": password,
            },
        )
        self.assertContains(get_access_token_response, "access", status_code=status.HTTP_200_OK)

        get_refresh_token_response = self.client.post(
            path=reverse("account:token_refresh"),
            data={
                "refresh": get_access_token_response.json()["refresh"],
            },
        )
        self.assertContains(get_refresh_token_response, "access", status_code=status.HTTP_200_OK)

    # RÉCUPÉRATION
        headers = {"Authorization": "Bearer " + get_access_token_response.json()["access"]}
        get_current_account_response = self.client.get(
            path=reverse("account:current_user"),
            headers=headers,
        )
        self.assertContains(get_current_account_response, "id", status_code=status.HTTP_200_OK)


@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}})
class TestCharacteristicsAPI(APITestCase):
    fixtures = [
        "fixtures/users.json",
        "fixtures/characteristics.json",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.sample_characteristic_type = get_random_characteristic_type()
        cls.sample_characteristic = get_random_characteristic()

    def test_get_characteristic_types(self):
        characteristic_type_list_response = self.client.get(
            path=reverse("characteristics:characteristic-type-list"),
        )
        self.assertEqual(status.HTTP_200_OK, characteristic_type_list_response.status_code)

        characteristic_type_detail_response = self.client.get(
            path=reverse("characteristics:characteristic-type-detail", kwargs={"pk": self.sample_characteristic_type.id}),
        )
        self.assertEqual(status.HTTP_200_OK, characteristic_type_detail_response.status_code)

    def test_get_characteristics(self):
        characteristic_list_response = self.client.get(
            path=reverse("characteristics:characteristic-list"),
        )
        self.assertEqual(status.HTTP_200_OK, characteristic_list_response.status_code)

        characteristic_detail_response = self.client.get(
            path=reverse("characteristics:characteristic-detail", kwargs={"pk": self.sample_characteristic.id}),
        )
        self.assertEqual(status.HTTP_200_OK, characteristic_detail_response.status_code)


@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}})
class TestFictionsAPI(APITestCase):
    fixtures = [
        "fixtures/users.json",
        "fixtures/characteristics.json",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.sample_user = sample_user()
        cls.sample_fiction = sample_fiction()

    def setUp(self) -> None:
        super().setUp()
        self.client.force_authenticate(self.sample_user)

    def test_get_fictions(self):
        fiction_list_response = self.client.get(
            path=reverse("fictions:fiction-list"),
        )
        self.assertEqual(status.HTTP_200_OK, fiction_list_response.status_code)
        
        fiction_detail_response = self.client.get(
            path=reverse("fictions:fiction-detail", kwargs={"pk": self.sample_fiction.id}),
        )
        self.assertEqual(status.HTTP_200_OK, fiction_detail_response.status_code)

    def test_create_fiction(self):
        test_payload = {
            "title": "test fiction title",
            "summary": "test fiction summary",
            "summary_images": [
                {
                    "url": "https://picsum.photos/250/",
                    "is_adult_only": False,
                    "index": 1,
                    "display_height": 250,
                    "display_width": 250
                }
            ],
            "storynote": "test fiction storynote",
            "characteristics": [150, 131, 161],
            "status": 2,
            "first_chapter": {
                "title": "test chapter title",
                "start_note": "test chapter start note",
                "end_note": "test chapter end note",
                "text": "test chapter text",
                "text_images": [
                    {
                        "url": "https://picsum.photos/250/",
                        "is_adult_only": False,
                        "index": 1,
                        "display_height": 250,
                        "display_width": 250
                    },
                    {
                        "url": "https://picsum.photos/250/",
                        "is_adult_only": False,
                        "index": 2,
                        "display_height": 250,
                        "display_width": 250
                    }
                ]
            }
        }

        fiction_create_response = self.client.post(
            path=reverse("fictions:fiction-list"),
            data=test_payload,
        )

        self.assertEqual(status.HTTP_201_CREATED, fiction_create_response.status_code)

    ''' TODO
    def test_get_chapters(self):
        self.fail()

    def test_create_chapter(self):
        self.fail()

    def test_get_collections(self):
        self.fail()

    def test_create_collection(self):
        self.fail()
    '''
