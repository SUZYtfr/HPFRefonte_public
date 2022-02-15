from PIL import Image
import tempfile

from django.core.files.images import ImageFile

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from tests.samples import *

from users.serializers import UserSerializer, UserCardSerializer
from fictions.serializers import FictionCardSerializer, FictionSerializer, ChapterSerializer, ChapterCardSerializer, Chapter
from news.serializers import NewsSerializer, NewsArticle
from features.serializers import FeatureSerializer
from images.serializers import BannerSerializer, Banner


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_url(app_name, object_id=None):
    app_basename = app_name[:-1]

    if object_id:
        return reverse(f"{app_name}:{app_basename}-detail", args=[object_id])
    return reverse(f"{app_name}:{app_basename}-list")


def generate_chapters_url(fiction_id, chapter_id=None):
    if chapter_id:
        return reverse(f"fictions:chapter-detail", kwargs={"fiction_pk": fiction_id, "pk": chapter_id})
    return reverse(f"fictions:chapter-list", kwargs={"fiction_pk": fiction_id})


def generate_banner_url(banner_id=None):
    if banner_id:
        return reverse(f"images:banner-detail", args=[banner_id])
    return reverse(f"images:banner-list")


def generate_account_url(profile=False):
    if profile:
        return reverse(f"accounts:manage")
    return reverse(f"accounts:create")


def generate_token_url(refresh=False):
    if refresh:
        return reverse("accounts:token_refresh")
    return reverse(f"accounts:token_obtain_pair")


NEWS_LIST_URL = reverse("news:news-list")


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
                                               validation_status=Chapter.ChapterValidationStage.PUBLISHED)
        cls.published_fiction = cls.validated_chapter.fiction

        cls.unvalidated_chapter = sample_chapter(creation_user=cls.active_user,
                                                 validation_status=Chapter.ChapterValidationStage.DRAFT)  # tests pour TOUS LES AUTRES statuts ?
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

        validated_chapter_card_serializer = ChapterCardSerializer(self.validated_chapter, context={"request": self.request})
        unvalidated_chapter_card_serializer = ChapterCardSerializer(self.unvalidated_chapter, context={"request": self.request})
        validated_chapter_serializer = ChapterSerializer(self.validated_chapter, context={"request": self.request})

        res_1 = self.client.get(path=generate_chapters_url(fiction_id=self.validated_chapter.fiction.id))
        res_2 = self.client.get(path=generate_chapters_url(fiction_id=self.validated_chapter.fiction.id, chapter_id=self.validated_chapter.id))
        res_3 = self.client.get(path=generate_chapters_url(fiction_id=self.unvalidated_chapter.fiction.id, chapter_id=self.unvalidated_chapter.id))

        self.assertEqual(res_1.status_code, status.HTTP_200_OK)
        self.assertIn(validated_chapter_card_serializer.data, res_1.data["results"])
        self.assertNotIn(unvalidated_chapter_card_serializer.data, res_1.data["results"])
        self.assertEqual(res_2.status_code, status.HTTP_200_OK)
        self.assertEqual(res_2.data, validated_chapter_serializer.data)
        self.assertEqual(res_3.status_code, status.HTTP_404_NOT_FOUND)

    def test_news_api_returns_only_published_news(self):
        """Teste que l'API d'actualités renvoie uniquement les actualités publiées"""

        draft_news = sample_news(creation_user=self.active_user, status=NewsArticle.NewsStatus.DRAFT)
        pending_news = sample_news(creation_user=self.active_user, status=NewsArticle.NewsStatus.PENDING)
        published_news = sample_news(creation_user=self.active_user, status=NewsArticle.NewsStatus.PUBLISHED)

        res = self.client.get(NEWS_LIST_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotIn(NewsSerializer(draft_news).data, res.data["results"])
        self.assertNotIn(NewsSerializer(pending_news).data, res.data["results"])
        self.assertIn(NewsSerializer(published_news).data, res.data["results"])

    def test_features_api_returns_only_allowed_features(self):
        """Teste que l'API de caractéristiques renvoie uniquement les caractéristiques autorisées"""

        allowed_feature = sample_feature(creation_user=self.active_user, is_forbidden=False)
        banned_feature = sample_feature(creation_user=self.active_user, is_forbidden=True)

        allowed_feature_serializer = FeatureSerializer(allowed_feature, context={"request": self.request})
        banned_feature_serializer = FeatureSerializer(banned_feature, context={"request": self.request})

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
                    category=Banner.BannerType.WEBSITE,
                    src_path=valid_banner_image,
                    is_active=True,
                )
                inactive_banner = Banner.objects.create(
                    creation_user=self.active_user,
                    category=Banner.BannerType.WEBSITE,
                    src_path=valid_banner_image,
                    is_active=False,
                )

        active_banner_serializer = BannerSerializer(active_banner, context={"request": self.request})
        inactive_banner_serializer = BannerSerializer(inactive_banner, context={"request": self.request})

        res_1 = self.client.get(path=generate_banner_url())
        res_2 = self.client.get(path=generate_banner_url(active_banner.id))
        res_3 = self.client.get(path=generate_banner_url(inactive_banner.id))

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

        res1 = self.client.patch(generate_account_url(profile=True), payload_blank)
        is_same_password = self.user.check_password(self.user_password)
        res2 = self.client.patch(generate_account_url(profile=True), payload)
        is_new_password = self.user.check_password("new123pwd")

        self.assertEqual(res1.status_code, status.HTTP_200_OK)
        self.assertTrue(is_same_password)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertTrue(is_new_password)

    def test_token(self):
        """Teste qu'un utilisateur peut obtenir un jeton d'authentification JWT"""

        res = self.client.post(generate_token_url(), {"nickname": self.user.nickname, "password": self.user_password})
        self.assertContains(res, "access", status_code=status.HTTP_200_OK)

        res_2 = self.client.post(generate_token_url(refresh=True), {"refresh": res.data["refresh"]})
        self.assertContains(res_2, "access", status_code=status.HTTP_200_OK)
