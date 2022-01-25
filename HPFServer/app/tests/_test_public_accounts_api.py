from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import User

from tests.samples import *

CREATE_ACCOUNT_URL = reverse("accounts:create")
MANAGE_ACCOUNT_URL = reverse("accounts:manage")
LOGIN_URL = reverse("accounts:login")
MY_FICTIONS_URL = reverse("app:myfictions:myfiction-list")


class TestsAccountCreateAPI(APITestCase):
    """Testent le comportement public de l'API de création de comptes utilisateur"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def test_create_is_possible_by_unauth_user(self):
        """Teste la création d'un compte par un utilisateur non-authentifié"""
        payload = {
            "nickname": "Coucou",
            "realname": "Mohammed Lesecond",
            "email": "mohammed@lesecond.fr",
            "birthdate": "2001-05-05",
            "password": "MotDePasse0000"
        }

        res = self.client.post(CREATE_ACCOUNT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

        user = User.objects.get(nickname=payload["nickname"])
        self.assertEqual(user.nickname, payload["nickname"])
        self.assertEqual(user.realname, payload["realname"])
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.birthdate.strftime("%Y-%m-%d"), payload["birthdate"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_create_is_possible_by_auth_user(self):
        """Teste la création d'un compte même si un utilisateur est authentifié"""
        user = sample_user()
        self.client.force_authenticate(user)

        res = self.client.post(CREATE_ACCOUNT_URL, sample_user_create_payload())

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.get(**res.data))

    def test_realname_not_given_accepted(self):
        """Teste que le nom réel n'est pas obligatoire"""
        payload_no_realname = sample_user_create_payload(realname="")

        res = self.client.post(CREATE_ACCOUNT_URL, payload_no_realname)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["realname"], "")

    def test_password_length(self):
        """Teste que le mot de passe a une longueur valide"""
        payload_password_too_short = sample_user_create_payload(password=123)
        payload_password_too_long = sample_user_create_payload(password="MotDePasseBeaucoupPlusLongQueLaMoyenne")

        res1 = self.client.post(CREATE_ACCOUNT_URL, payload_password_too_short)
        self.assertEqual(res1.status_code, status.HTTP_400_BAD_REQUEST)

        res2 = self.client.post(CREATE_ACCOUNT_URL, payload_password_too_long)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)


class TestsAccountLoginAPI(APITestCase):
    """Testent le comportement public de l'API de connexion de comptes utilisateur"""

    def test_user_login_with_valid_credentials(self):
        """Teste qu'un utilisateur peut se connecter à un compte existant"""
        password = "Password123"
        user = sample_user(password=password)
        login_payload = {"nickname": user.nickname, "password": password}

        res = self.client.post(LOGIN_URL, login_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_user_login_to_inexistant_user(self):
        """Teste qu'un utilisateur ne peut pas se connecter à un compte inexistant"""
        login_payload = {"nickname": "ExistePas", "password": "rien123456"}
        res = self.client.post(LOGIN_URL, login_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_user_login_with_invalid_credentials(self):
        """Teste qu'un utilisateur ne peut pas se connecter avec un mauvais MDP"""
        user = sample_user()
        login_payload = {"nickname": user.nickname, "password": "mauvaisMDP"}

        res = self.client.post(LOGIN_URL, login_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)


class TestsAuthNeeded(APITestCase):
    """à trier"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_user_manage_not_accessible_if_unauth(self):
        """Teste que la page de gestion de compte est seulement accessible si identifié"""
        res = self.client.get(MANAGE_ACCOUNT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_need_for_personal_fictions_list_access(self):
        client = APIClient()
        res = client.get(path=MY_FICTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)