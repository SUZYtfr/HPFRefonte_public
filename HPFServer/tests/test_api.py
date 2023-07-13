from rest_framework.test import APITestCase, override_settings
from rest_framework.reverse import reverse
from rest_framework import status

from users.models import User


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

"""
class TestAPI(APITestCase):
    def test_users_api(self):
        self.fail()

    def test_fictions_api(self):
        self.fail()

    def test_characteristics_api(self):
        self.fail()
    
    def test_news_api(self):
        self.fail()

    def test_media_access(self):
        self.fail()
"""