from PIL import Image
import tempfile

from django.conf import settings
from django.core.files.images import ImageFile
from django.contrib.auth.models import Permission

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status

from tests.samples import *

from users.serializers import UserSerializer, UserCardSerializer
from fictions.serializers import FictionCardSerializer, FictionSerializer, Fiction, ChapterSerializer, ChapterCardSerializer, Chapter
from news.serializers import NewsSerializer, NewsArticle
from characteristics.serializers import CharacteristicSerializer
from images.serializers import BannerSerializer, Banner

import logging


def generate_url(app_name, pk=None, **kwargs):
    comp = app_name.split(".")

    if pk:
        kwargs.update({"pk": pk})
        return reverse(f"{comp[0]}:{comp[-1][:-1]}-detail", kwargs=kwargs)
    return reverse(f"{comp[0]}:{comp[-1][:-1]}-list", kwargs=kwargs)


def generate_account_url(profile=False):
    if profile:
        return reverse(f"accounts:manage")
    return reverse(f"accounts:create")


def generate_token_url(refresh=False):
    if refresh:
        return reverse("accounts:token_refresh")
    return reverse(f"accounts:token_obtain_pair")


def generate_news_url(news_id=None):
    if news_id:
        return reverse("news:news-detail", args=[news_id])
    return reverse("news:news-list")


def generate_chapter_submit_url(**kwargs):
    return reverse(f"fictions:chapter-submit", kwargs=kwargs)


def generate_chapter_validate_url(**kwargs):
    return reverse(f"fictions:chapter-validate", kwargs=kwargs)


def generate_chapter_invalidate_url(**kwargs):
    return reverse(f"fictions:chapter-invalidate", kwargs=kwargs)


def generate_fiction_authors_url(**kwargs):
    return reverse(f"fictions:fiction-authors", kwargs=kwargs)


class TestsPublicAPI(APITestCase):
    """Testent le comportement de l'API publique"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get('/')

        cls.active_user = sample_user()

        cls.validated_chapter = sample_chapter(creation_user=cls.active_user,
                                               validation_status=Chapter.ValidationStage.PUBLISHED)
        cls.published_fiction = cls.validated_chapter.fiction

        cls.unvalidated_chapter = sample_chapter(creation_user=cls.active_user,
                                                 validation_status=Chapter.ValidationStage.DRAFT)  # tests pour TOUS LES AUTRES statuts ?
        cls.unpublished_fiction = cls.unvalidated_chapter.fiction

    def test_user_api_returns_only_active_users(self):
        """Teste que l'api des membres renvoie uniquement les membres actifs"""

        self.inactive_user = sample_user()
        self.inactive_user.is_active = False
        self.inactive_user.save()

        active_user_serializer = UserCardSerializer(self.active_user, context={"request": self.request})
        active_user_card_serializer = UserSerializer(self.active_user, context={"request": self.request})
        inactive_user_serializer = UserCardSerializer(self.inactive_user, context={"request": self.request})

        res_1 = self.client.get(path=generate_url("users"))
        res_2 = self.client.get(path=generate_url("users", self.active_user.id))
        res_3 = self.client.get(path=generate_url("users", self.inactive_user.id))

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertIn(active_user_serializer.data, res_1.data["results"])
        self.assertNotIn(inactive_user_serializer.data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(active_user_card_serializer.data, res_2.data)
        self.assertEqual(res_3.status_code, status.HTTP_404_NOT_FOUND)

    def test_fiction_api_returns_only_published_fictions(self):
        """Teste que l'api de fictions renvoie uniquement les fictions publiées"""

        published_fiction_card_serializer = FictionCardSerializer(self.published_fiction, context={"request": self.request})
        unpublished_fiction_card_serializer = FictionCardSerializer(self.unpublished_fiction, context={"request": self.request})
        published_fiction_serializer = FictionSerializer(self.published_fiction, context={"request": self.request})

        res_1 = self.client.get(path=generate_url("fictions"))
        res_2 = self.client.get(path=generate_url("fictions", self.published_fiction.id))
        res_3 = self.client.get(path=generate_url("fictions", self.unpublished_fiction.id))

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertIn(published_fiction_card_serializer.data, res_1.data["results"])
        self.assertNotIn(unpublished_fiction_card_serializer.data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.data, published_fiction_serializer.data)
        self.assertEqual(res_3.status_code, status.HTTP_404_NOT_FOUND)

    def test_fiction_api_returns_only_validated_chapters(self):
        """Teste que l'API de fictions renvoie uniquement les chapitres validés"""

        res_1 = self.client.get(path=generate_url("fictions.chapters", fiction_pk=self.validated_chapter.fiction.id))
        res_2 = self.client.get(path=generate_url("fictions.chapters", self.validated_chapter.id, fiction_pk=self.validated_chapter.fiction.id))
        res_3 = self.client.get(path=generate_url("fictions.chapters", self.unvalidated_chapter.id, fiction_pk=self.unvalidated_chapter.fiction.id))

        self.validated_chapter.refresh_from_db(fields=["read_count"])

        validated_chapter_card_serializer = ChapterCardSerializer(self.validated_chapter, context={"request": self.request})
        unvalidated_chapter_card_serializer = ChapterCardSerializer(self.unvalidated_chapter, context={"request": self.request})
        validated_chapter_serializer = ChapterSerializer(self.validated_chapter, context={"request": self.request})

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertIn(validated_chapter_card_serializer.data, res_1.data["results"])
        self.assertNotIn(unvalidated_chapter_card_serializer.data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.data, validated_chapter_serializer.data)
        self.assertEqual(res_3.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_api_returns_only_published_news(self):
        """Teste que l'API d'actualités renvoie uniquement les actualités publiées"""

        draft_news = sample_news(creation_user=self.active_user, status=NewsArticle.Status.DRAFT)
        pending_news = sample_news(creation_user=self.active_user, status=NewsArticle.Status.PENDING)
        published_news = sample_news(creation_user=self.active_user, status=NewsArticle.Status.PUBLISHED)

        res = self.client.get(generate_news_url())

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(NewsSerializer(draft_news).data, res.data["results"])
        self.assertNotIn(NewsSerializer(pending_news).data, res.data["results"])
        self.assertIn(NewsSerializer(published_news).data, res.data["results"])

    def test_features_api_returns_only_allowed_features(self):
        """Teste que l'API de caractéristiques renvoie uniquement les caractéristiques autorisées"""

        allowed_feature = sample_feature(creation_user=self.active_user, is_forbidden=False)
        banned_feature = sample_feature(creation_user=self.active_user, is_forbidden=True)

        allowed_feature_serializer = CharacteristicSerializer(allowed_feature, context={"request": self.request})
        banned_feature_serializer = CharacteristicSerializer(banned_feature, context={"request": self.request})

        res_1 = self.client.get(path=generate_url("features"))
        res_2 = self.client.get(path=generate_url("features", allowed_feature.id))
        res_3 = self.client.get(path=generate_url("features", banned_feature.id))

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertIn(allowed_feature_serializer.data, res_1.data["results"])
        self.assertNotIn(banned_feature_serializer.data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.data, allowed_feature_serializer.data)
        self.assertEqual(res_3.status_code, status.HTTP_404_NOT_FOUND)

    def test_banners_api_returns_only_active_banners(self):
        """Teste que l'API de caractéristiques renvoie uniquement les caractéristiques autorisées"""

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (468, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            with ImageFile(ntf.file, name="test_banner.jpg") as valid_banner_image:
                active_banner = Banner.objects.create(
                    creation_user=self.active_user,
                    category=Banner.Type.WEBSITE,
                    src_path=valid_banner_image,
                    is_active=True,
                )
                inactive_banner = Banner.objects.create(
                    creation_user=self.active_user,
                    category=Banner.Type.WEBSITE,
                    src_path=valid_banner_image,
                    is_active=False,
                )

        active_banner_serializer = BannerSerializer(active_banner, context={"request": self.request})
        inactive_banner_serializer = BannerSerializer(inactive_banner, context={"request": self.request})

        res_1 = self.client.get(path=generate_url("images.banners"))
        res_2 = self.client.get(path=generate_url("images.banners", active_banner.id))
        res_3 = self.client.get(path=generate_url("images.banners", inactive_banner.id))

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertIn(active_banner_serializer.data, res_1.data["results"])
        self.assertNotIn(inactive_banner_serializer.data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.data, active_banner_serializer.data)
        self.assertEqual(res_3.status_code, status.HTTP_404_NOT_FOUND)


class TestsAccountAPI(APITestCase):
    """Testent le comportement de l'API de compte utilisateur"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_password = "password1234"
        cls.user = sample_user(password=cls.user_password)
        cls.client = APIClient()
        # cls.token = str(RefreshToken.for_user(cls.user).access_token)

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)

    def test_password_change(self):
        """Teste que le mot de passe n'est pas obligatoire pour modifier le compte"""

        payload_blank = {
            "password": None
        }

        payload = {
            "password": "new123pwd",
        }

        res_1 = self.client.patch(generate_account_url(profile=True), payload_blank)
        self.user.refresh_from_db(fields=["password"])
        is_same_password = self.user.check_password(self.user_password)

        res_2 = self.client.patch(generate_account_url(profile=True), payload)
        self.user.refresh_from_db(fields=["password"])
        is_new_password = self.user.check_password("new123pwd")

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertTrue(is_same_password)
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertTrue(is_new_password)

    def test_user_can_get_token(self):
        """Teste qu'un utilisateur peut obtenir un jeton d'authentification JWT"""

        res = self.client.post(generate_token_url(), {"username": self.user.username, "password": self.user_password})
        self.assertContains(res, "access", status_code=status.HTTP_200_OK)

        res_2 = self.client.post(generate_token_url(refresh=True), {"refresh": res.data["refresh"]})
        self.assertContains(res_2, "access", status_code=status.HTTP_200_OK)

    def test_user_cannot_change_username(self):
        """Teste qu'un utilisateur ne peut pas modifier son pseudo"""

        res = self.client.patch(generate_account_url(profile=True), {"username": "NickTheName"})

        self.user.refresh_from_db(fields=["username"])

        self.assertEqual(res.status_code, status.HTTP_200_OK)  # les paramètres inconnus sont ignorés
        self.assertNotEqual(self.user.username, "NickTheName")


class TestsUserAPI(APITestCase):
    """Testent le comportement de l'API de membre"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = sample_user()
        cls.unvalidated_fiction = sample_fiction(creation_user=cls.user)

        cls.client = APIClient()

        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get('/')

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.user)

    def test_auth_user_can_control_all_own_fictions(self):
        """Teste qu'un membre a le contrôle sur toutes ses fictions"""

        payload = {
            "title": "Test title",
            "features": random_valid_feature_id_list(),
        }

        res_1 = self.client.post(generate_url("fictions"), payload)

        self.assertContains(res_1, "id", status_code=status.HTTP_201_CREATED)

        fiction = Fiction.objects.get(pk=res_1.data.get("id"))

        res_2 = self.client.get(generate_url("fictions"), {"mine": True})
        res_3 = self.client.get(generate_url("fictions", fiction.id), {"mine": True})
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertIn(FictionCardSerializer(fiction, context={"request": self.request}).data, res_2.data["results"])
        self.assertEqual(res_3.status_code, status.HTTP_200_OK)
        self.assertEqual(FictionSerializer(fiction, context={"request": self.request}).data, res_3.data)

        res_4 = self.client.patch(generate_url("fictions", fiction.id), {"title": "Test title 2"}, **{"QUERY_STRING": "mine=True"})
        self.assertEqual(res_4.status_code, status.HTTP_200_OK)

        res_5 = self.client.delete(generate_url("fictions", fiction.id), **{"QUERY_STRING": "mine=True"})
        self.assertEqual(res_5.status_code, status.HTTP_204_NO_CONTENT)

    def test_auth_user_can_control_all_own_chapters(self):
        """Teste qu'un membre a le contrôle sur tous ses chapitres"""

        payload = {
            "title": "Test title",
            "text": "Test texte",
            "text_file_upload": None,
        }

        res_1 = self.client.post(generate_url("fictions.chapters", fiction_pk=self.unvalidated_fiction.id), payload)

        self.assertContains(res_1, "id", status_code=status.HTTP_201_CREATED)

        chapter = Chapter.objects.get(pk=res_1.data.get("id"))

        res_2 = self.client.get(generate_url("fictions.chapters", fiction_pk=chapter.fiction.id), {"mine": True})
        res_3 = self.client.get(generate_url("fictions.chapters", chapter.id, fiction_pk=chapter.fiction.id), {"mine": True})
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertIn(ChapterCardSerializer(chapter, context={"request": self.request}).data, res_2.data["results"])
        self.assertEqual(res_3.status_code, status.HTTP_200_OK)
        self.assertEqual(ChapterSerializer(chapter, context={"request": self.request}).data, res_3.data)

        res_4 = self.client.patch(generate_url("fictions.chapters", chapter.id, fiction_pk=chapter.fiction.id), {"title": "Test title 2", "text_file_upload": None, "text": "bla"}, **{"QUERY_STRING": "mine=True"})
        self.assertEqual(res_4.status_code, status.HTTP_200_OK)

        res_5 = self.client.delete(generate_url("fictions.chapters", chapter.id, fiction_pk=chapter.fiction.id), **{"QUERY_STRING": "mine=True"})
        self.assertEqual(res_5.status_code, status.HTTP_204_NO_CONTENT)

    def test_auth_user_can_submit_own_chapter(self):
        """Teste qu'un membre peut envoyer son chapitre à la validation"""

        draft_chapter = sample_chapter(creation_user=self.user)

        res_1 = self.client.put(generate_chapter_submit_url(pk=draft_chapter.id,
                                                            fiction_pk=draft_chapter.fiction.id),
                                **{"QUERY_STRING": "mine=True"})
        res_2 = self.client.put(generate_chapter_submit_url(pk=draft_chapter.id,
                                                            fiction_pk=draft_chapter.fiction.id),
                                **{"QUERY_STRING": "mine=True"})

        self.assertContains(res_1, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_1.data["validation_status"], Chapter.ValidationStage.PENDING)
        self.assertEqual(res_2.status_code, status.HTTP_403_FORBIDDEN)

    def test_premium_user_validates_automatically(self):
        """Teste qu'un adhérent valide son chapitre automatiquement"""

        premium_user = sample_user()
        premium_user.user_permissions.add(Permission.objects.get(codename="automatic_validation"))
        premium_draft_chapter = sample_chapter(creation_user=premium_user)
        premium_edit_required_chapter = sample_chapter(creation_user=premium_user,
                                                       fiction=premium_draft_chapter.fiction,
                                                       validation_status=Chapter.ValidationStage.EDIT_REQUIRED)

        self.client.force_authenticate(premium_user)

        res_1 = self.client.put(generate_chapter_submit_url(pk=premium_draft_chapter.id,
                                                            fiction_pk=premium_draft_chapter.fiction.id),
                                **{"QUERY_STRING": "mine=True"})
        res_2 = self.client.put(generate_chapter_submit_url(pk=premium_edit_required_chapter.id,
                                                            fiction_pk=premium_edit_required_chapter.fiction.id),
                                **{"QUERY_STRING": "mine=True"})

        self.assertContains(res_1, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_1.data["validation_status"], Chapter.ValidationStage.PUBLISHED)
        self.assertContains(res_2, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_2.data["validation_status"], Chapter.ValidationStage.EDITED)

    def test_first_author_can_add_more_authors(self):

        user_2 = sample_user()
        user_3 = sample_user()

        res_1 = self.client.put(generate_fiction_authors_url(pk=self.unvalidated_fiction.id), {"author_username": user_2.username}, **{"QUERY_STRING": "mine=True"})

        self.client.force_authenticate(user_2)

        res_2 = self.client.put(generate_fiction_authors_url(pk=self.unvalidated_fiction.id), {"author_username": user_3.username}, **{"QUERY_STRING": "mine=True"})

        self.assertContains(res_1, "authors", status_code=status.HTTP_200_OK)
        self.assertIn(user_2, self.unvalidated_fiction.authors.all())
        self.assertEqual(res_2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn(user_3, self.unvalidated_fiction.authors.all())


class TestsModeratorAPI(APITestCase):
    """Testent le comportement de l'API de modération"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = sample_user()

        cls.moderator = sample_user()
        cls.moderator.user_permissions.set([
            Permission.objects.get(codename="view_fiction"),
            Permission.objects.get(codename="change_fiction"),
            Permission.objects.get(codename="delete_fiction"),
            Permission.objects.get(codename="view_chapter"),
            Permission.objects.get(codename="change_chapter"),
            Permission.objects.get(codename="delete_chapter"),
            Permission.objects.get(codename="staff_validation"),
        ])

        cls.unvalidated_fiction = sample_fiction(cls.user)
        cls.draft_chapter = sample_chapter(creation_user=cls.user,
                                           validation_status=Chapter.ValidationStage.DRAFT)
        cls.unvalidated_chapter = sample_chapter(creation_user=cls.user,
                                                 fiction=cls.draft_chapter.fiction,
                                                 validation_status=Chapter.ValidationStage.PENDING)

        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get('/')

    def setUp(self) -> None:
        self.client.force_authenticate(user=self.moderator)

    def test_moderator_can_control_all_fictions(self):
        """Teste qu'un modérateur a le contrôle sur toutes les fictions"""

        res_1 = self.client.get(generate_url("fictions"))
        res_2 = self.client.get(generate_url("fictions", self.unvalidated_fiction.id))

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertIn(FictionCardSerializer(self.unvalidated_fiction, context={"request": self.request}).data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(FictionSerializer(self.unvalidated_fiction, context={"request": self.request}).data, res_2.data)

        res_3 = self.client.patch(generate_url("fictions", self.unvalidated_fiction.id), {"title": "Test title 2"})
        self.assertEqual(res_3.status_code, status.HTTP_200_OK)

        res_4 = self.client.delete(generate_url("fictions", self.unvalidated_fiction.id))
        self.assertEqual(res_4.status_code, status.HTTP_204_NO_CONTENT)

    def test_moderator_can_control_all_chapters_but_drafts(self):
        """Teste qu'un modérateur a le contrôle sur tous les chapitres sauf les brouillons"""

        res_1 = self.client.get(generate_url("fictions.chapters", fiction_pk=self.draft_chapter.fiction.id))
        res_2 = self.client.get(generate_url("fictions.chapters", self.draft_chapter.id, fiction_pk=self.draft_chapter.fiction.id))
        res_3 = self.client.get(generate_url("fictions.chapters", self.unvalidated_chapter.id, fiction_pk=self.unvalidated_chapter.fiction.id))

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertNotIn(ChapterCardSerializer(self.draft_chapter, context={"request": self.request}).data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res_3.status_code, status.HTTP_200_OK)
        self.assertEqual(ChapterSerializer(self.unvalidated_chapter, context={"request": self.request}).data, res_3.data)

        res_4 = self.client.patch(generate_url("fictions.chapters", self.unvalidated_chapter.id, fiction_pk=self.unvalidated_chapter.fiction.id), {"title": "Test title 2", "text_file_upload": None, "text": "bla"})
        self.assertEqual(res_4.status_code, status.HTTP_200_OK)

        res_5 = self.client.delete(generate_url("fictions.chapters", self.unvalidated_chapter.id, fiction_pk=self.unvalidated_chapter.fiction.id))
        self.assertEqual(res_5.status_code, status.HTTP_204_NO_CONTENT)

    def test_moderator_can_validate_chapters(self):
        """Teste qu'un modérateur peut valider des chapitres"""

        draft_chapter = sample_chapter(creation_user=self.user, validation_status=Chapter.ValidationStage.DRAFT)
        res_1 = self.client.put(generate_chapter_validate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        draft_chapter.validation_status = Chapter.ValidationStage.PENDING
        draft_chapter.save()

        res_2 = self.client.put(generate_chapter_validate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        draft_chapter.validation_status = Chapter.ValidationStage.EDIT_REQUIRED
        draft_chapter.save()

        res_3 = self.client.put(generate_chapter_validate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        draft_chapter.validation_status = Chapter.ValidationStage.EDITED
        draft_chapter.save()

        res_4 = self.client.put(generate_chapter_validate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        self.assertEqual(res_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertContains(res_2, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_2.data["validation_status"], Chapter.ValidationStage.PUBLISHED)
        self.assertEqual(res_3.status_code, status.HTTP_403_FORBIDDEN)
        self.assertContains(res_4, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_4.data["validation_status"], Chapter.ValidationStage.PUBLISHED)

    def test_moderator_can_invalidate_chapters(self):
        """Teste qu'un modérateur peut invalider des chapitres"""

        draft_chapter = sample_chapter(creation_user=self.user, validation_status=Chapter.ValidationStage.DRAFT)
        res_1 = self.client.put(generate_chapter_invalidate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        draft_chapter.validation_status = Chapter.ValidationStage.PENDING
        draft_chapter.save()

        res_2 = self.client.put(generate_chapter_invalidate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        draft_chapter.validation_status = Chapter.ValidationStage.EDIT_REQUIRED
        draft_chapter.save()

        res_3 = self.client.put(generate_chapter_invalidate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        draft_chapter.validation_status = Chapter.ValidationStage.EDITED
        draft_chapter.save()

        res_4 = self.client.put(generate_chapter_invalidate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        draft_chapter.validation_status = Chapter.ValidationStage.PUBLISHED
        draft_chapter.save()

        res_5 = self.client.put(generate_chapter_invalidate_url(pk=draft_chapter.id, fiction_pk=draft_chapter.fiction.id))

        self.assertEqual(res_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertContains(res_2, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_2.data["validation_status"], Chapter.ValidationStage.EDIT_REQUIRED)
        self.assertEqual(res_3.status_code, status.HTTP_403_FORBIDDEN)
        self.assertContains(res_4, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_4.data["validation_status"], Chapter.ValidationStage.EDIT_REQUIRED)
        self.assertContains(res_5, "validation_status", status_code=status.HTTP_200_OK)
        self.assertEqual(res_5.data["validation_status"], Chapter.ValidationStage.EDIT_REQUIRED)


class TestsNewsCreatorAPI(APITestCase):
    """Testent le comportement de l'API de créateur de news"""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.news_creator = sample_user()
        cls.news_creator.user_permissions.set([
            Permission.objects.get(codename="add_newsarticle"),
            Permission.objects.get(codename="view_newsarticle"),
            Permission.objects.get(codename="change_newsarticle"),
            Permission.objects.get(codename="delete_newsarticle"),
        ])

        cls.client = APIClient()

    def setUp(self) -> None:
        self.client.force_authenticate(self.news_creator)

    def test_news_creator_can_controll_all_news(self):
        """Teste qu'un créateur de news a le contrôle sur toutes les news"""

        payload = {
            "title": "Test title",
            "content": "Test content",
            "category": NewsArticle.Category.UNDEFINED,
        }

        res_1 = self.client.post(generate_news_url(), payload)

        self.assertContains(res_1, "id", status_code=status.HTTP_201_CREATED)

        news = NewsArticle.objects.get(pk=res_1.data.get("id"))

        res_2 = self.client.get(generate_news_url())
        res_3 = self.client.get(generate_news_url(news.id))
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertIn(NewsSerializer(news).data, res_2.data["results"])
        self.assertEqual(res_3.status_code, status.HTTP_200_OK)
        self.assertEqual(NewsSerializer(news).data, res_3.data)

        res_4 = self.client.patch(generate_news_url(news.id), {"title": "Test title 2"})
        self.assertEqual(res_4.status_code, status.HTTP_200_OK)

        res_5 = self.client.delete(generate_news_url(news.id))
        self.assertEqual(res_5.status_code, status.HTTP_204_NO_CONTENT)


class TestsReviewAPI(APITestCase):
    """Testent les modèles de reviews et de réponses à reviews"""

    @staticmethod
    def generate_object_review_url(model, object_pk):
        return reverse(f"reviews:{model}:object-review-list", kwargs={"object_pk": object_pk})

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.chapter = sample_chapter(creation_user=cls.author,
                                     validation_status=Chapter.ValidationStage.PUBLISHED)
        cls.fiction = cls.chapter.fiction
        cls.reviewer = sample_user()
        cls.staff_user = sample_user()
        cls.staff_user.user_permissions.add(
            Permission.objects.get(codename="can_post_review_as_staff")
        )

        cls.client = APIClient()

    def test_review_creation_permissions(self):
        """Teste les permissions de création de reviews"""

        payload = {
            "text": "Test texte",
            "grading": 10,
            "draft": False,
        }

        self.client.force_authenticate(self.reviewer)
        # 1 review = ok
        res_1 = self.client.post(self.generate_object_review_url("users", self.author.id), payload)
        # 2 reviews sur le même objet = FAIL
        res_2 = self.client.post(self.generate_object_review_url("users", self.author.id), payload)
        # review sur soi-même = FAIL
        res_3 = self.client.post(self.generate_object_review_url("users", self.reviewer.id), payload)

        self.assertContains(res_1, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(res_2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res_3.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_user_can_post_review_as_staff(self):
        """Teste qu'un modérateur peut poster une review en utilisant le compte de modération"""

        payload = {
            "draft": False,
            "text": "Test Text",
            "grading": None
        }

        payload_as_staff = payload.copy()
        payload_as_staff["as_staff"] = True

        payload_as_staff_with_draft = payload_as_staff.copy()
        payload_as_staff_with_draft["draft"] = True

        self.client.force_authenticate(self.staff_user)
        res_2 = self.client.post(self.generate_object_review_url("chapters", self.chapter.id), payload_as_staff)
        res_3 = self.client.post(self.generate_object_review_url("chapters", self.chapter.id), payload_as_staff_with_draft)
        res_1 = self.client.post(self.generate_object_review_url("chapters", self.chapter.id), payload)

        self.assertContains(res_1, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(res_1.data["creation_user"], self.staff_user.id)
        self.assertContains(res_2, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(res_2.data["creation_user"], settings.MODERATION_ACCOUNT_ID)
        self.assertContains(res_3, "non_field_errors", status_code=status.HTTP_400_BAD_REQUEST)

    def test_anonymous_can_post_reviews(self):
        """Teste qu'un visiteur peut poster une review"""

        payload = {
            "email": "anonyme@example.example",
            "text": "Test Text",
            "grading": None
        }

        # 1 review anonyme = ok
        res_1 = self.client.post(self.generate_object_review_url("fictions", self.fiction.id), payload)
        # 2 reviews anonymes = FAIL
        res_2 = self.client.post(self.generate_object_review_url("fictions", self.fiction.id), payload)
        # review anonyme avec email de membre actif = FAIL
        res_3 = self.client.post(self.generate_object_review_url("fictions", self.fiction.id), payload)

        self.assertContains(res_1, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(res_2.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res_3.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authors_can_reply_to_reviews(self):
        """Teste qu'un auteur peut répondre à une review le concernant"""

        review = sample_review(self.reviewer, work=self.fiction, draft=False)

        payload = {
            "text": "Test Réponse",
        }

        self.client.force_authenticate(self.reviewer)
        res_1 = self.client.post(generate_url("reviews.replys", review_pk=review.id), payload)
        self.client.force_authenticate(self.author)
        res_2 = self.client.post(generate_url("reviews.replys", review_pk=review.id), payload)
        self.client.force_authenticate(self.author)
        res_3 = self.client.post(generate_url("reviews.replys", review_pk=review.id), payload)

        self.assertEqual(res_1.status_code, status.HTTP_403_FORBIDDEN)
        self.assertContains(res_2, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(res_3.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_reply_to_reviews(self):
        """Teste qu'un modérateur peut répondre à une review avec le compte de modération"""

        review = sample_review(self.reviewer, work=self.fiction, draft=False)

        payload = {
            "text": "Test Réponse",
            "as_staff": True,
        }

        self.client.force_authenticate(self.staff_user)
        res_1 = self.client.post(generate_url("reviews.replys", review_pk=review.id), payload)
        res_2 = self.client.post(generate_url("reviews.replys", review_pk=review.id), payload)
        self.assertContains(res_1, "id", status_code=status.HTTP_201_CREATED)
        self.assertEqual(res_2.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self) -> None:
        self.client.force_authenticate()
        self.reviewer.reviews.all().delete()
