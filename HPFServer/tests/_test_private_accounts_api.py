from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts.serializers import PrivateAccountManagementSerializer

from tests.samples import *

MANAGE_ACCOUNT_URL = reverse("accounts:manage")


class TestsAccountManageAPI(APITestCase):
    """Teste le comportement privé de l'API de gestion de comptes utilisateur"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def setUp(self) -> None:
        self.user = sample_user()
        self.client.force_authenticate(self.user)

    def test_user_manage_accessible_if_auth(self):
        """Teste que la page de gestion de compte est accessible si identifié"""
        serializer = PrivateAccountManagementSerializer(self.user)
        res = self.client.get(path=MANAGE_ACCOUNT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
        self.assertNotIn("password", res.data)

    def test_user_can_edit_account(self):
        """Teste que l'utilisateur peut modifier les informations de son compte"""
        payload = sample_user_edit_payload()

        res = self.client.patch(MANAGE_ACCOUNT_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.realname, payload["realname"])
        self.assertEqual(self.user.birthdate.strftime("%Y-%m-%d"), payload["birthdate"])
        self.assertEqual(self.user.email, payload["email"])
        self.assertTrue(self.user.check_password(payload["password"])),
        self.assertEqual(self.user.age_consent, payload["age_consent"])
        self.assertEqual(self.user.bio, payload["bio"]),
        self.assertEqual(self.user.gender, payload["sex"])

    def test_user_cannot_edit_nickname(self):
        """Teste que l'utilisateur ne peut pas modifier son pseudo"""
        payload_edit_nickname = sample_user_edit_payload()
        payload_edit_nickname.update({"nickname": "NickTheName"})

        res = self.client.patch(MANAGE_ACCOUNT_URL, payload_edit_nickname)

        self.user.refresh_from_db()

        # Les clés supplémentaires sont simplement ignorées : Pas d'erreur
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.user.nickname, payload_edit_nickname["nickname"])

    def test_password_not_mandatory_for_editing_profile(self):
        """Teste que le mot de passe n'est pas obligatoire pour modifier un profil"""
        password = self.user.password

        payload = sample_user_edit_payload(password="")

        res = self.client.patch(MANAGE_ACCOUNT_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.password, password)

    def tearDown(self) -> None:
        # Ceci "déconnecte" l'utilisateur
        self.client.force_authenticate()
        self.user.delete()
