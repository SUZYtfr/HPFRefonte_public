from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from django.contrib.auth.models import Group
from reviews.models import Review, ReviewReply

from reviews.models import MIN_GRADING_VALUE, MAX_GRADING_VALUE

from core.utils import get_moderation_account

from tests.samples import *


class TestsReviewPosting(APITestCase):
    """Testent la création de reviews"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")

        cls.fiction = sample_fiction()
        cls.fiction_reviews_url = reverse("app:reviews:fiction-reviews", args=[cls.fiction.id])

        cls.normal_user = sample_user(is_staff=False)

        cls.moderation_group = Group.objects.get(name__contains="modération")
        cls.staff_user = sample_user(is_staff=True)
        cls.staff_user.groups.add(cls.moderation_group)

    def test_member_creates_review(self):
        """Teste qu'un membre peut poster une review"""

        payload = {
            "draft": False,
            "text": "Exemple de texte de review",
        }

        self.client.force_authenticate(self.normal_user)
        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual(self.normal_user.username, self.fiction.reviews.get(id=res.data["id"]).creation_user.username)

    def test_anonymous_creates_review(self):
        """Teste qu'un anonyme peut poster une review"""

        payload = {
            "email": "fake@email.com",
            "text": "Exemple de texte de review",
        }

        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual("[anonyme]", self.fiction.reviews.get(id=res.data["id"]).creation_user.username)

    # TODO - réparer l'assignation des permissions dans initial pour réparer ce test
    def test_staff_creates_review_as_staff(self):
        """Teste qu'un modérateur peut poster une review avec le compte de modération"""

        payload = {
            "draft": False,
            "text": "Exemple de texte de review.",
            "as_staff": True,
        }

        self.client.force_authenticate(self.staff_user)
        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_201_CREATED)
        self.assertEqual(res.data["creation_user"], get_moderation_account().id)

    # def test_non_staff_cannot_create_review_as_staff(self):
    #     """Teste qu'un membre ou un anonyme ne peuvent pas poster de review avec le compte de modération"""
    #
    #     anonymous_user_payload = {
    #         "email": "another@fakemail.com",
    #         "as_staff": True,
    #         "text": "Exemple de texte de review.",
    #     }
    #
    #     normal_user_payload = {
    #         "draft": False,
    #         "as_staff": True,
    #         "text": "Exemple de texte de review.",
    #     }
    #
    #     res1 = self.client.post(self.fiction_reviews_url, anonymous_user_payload)
    #     self.client.force_authenticate(self.normal_user)
    #     res2 = self.client.post(self.fiction_reviews_url, normal_user_payload)
    #
    #     self.assertEqual(res1.status_code, HTTP_201_CREATED)
    #     self.assertEqual("[anonyme]", self.fiction.reviews.get(id=res1.data["id"]).creation_user.username)
    #     self.assertEqual(res2.status_code, HTTP_201_CREATED)
    #     self.assertEqual(self.normal_user.username, self.fiction.reviews.get(id=res2.data["id"]).creation_user.username)

    def tearDown(self) -> None:
        self.client.force_authenticate(None)  # désauthentifie entre les tests


class TestsReviewPostingPermissions(APITestCase):
    """Testent les permissions de création de reviews"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")

        cls.author = sample_user()
        cls.fiction = sample_fiction(creation_user=cls.author)
        cls.fiction_reviews_url = reverse("app:reviews:fiction-reviews", args=[cls.fiction.id])

        cls.normal_user = sample_user()

    def test_authors_cannot_review_themselves(self):
        """Teste qu'un auteur ne peut pas se reviewer lui-même ou ses œuvres"""

        payload = {
            "draft": False,
            "text": "Exemple de texte de review."
        }

        self.client.force_authenticate(self.author)

        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)
        self.assertNotIn("id", res.data)

    def test_reviewer_can_only_review_once_per_object(self):
        """Teste qu'une seule review peut être écrite par reviewer et par objet"""

        payload = {
            "draft": False,
            "text": "Exemple de texte de review."
        }

        self.client.force_authenticate(self.normal_user)
        self.client.post(self.fiction_reviews_url, payload)

        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)
        self.assertNotIn("id", res.data)

    def tearDown(self) -> None:
        self.client.force_authenticate(None)


class TestsReviewGradingValidation(APITestCase):
    """Testent les validateurs de notation dans les reviews"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")

        cls.fiction = sample_fiction()
        cls.fiction_reviews_url = reverse("app:reviews:fiction-reviews", args=[cls.fiction.id])

        cls.normal_user = sample_user()

    def setUp(self) -> None:
        self.client.force_authenticate(self.normal_user)

    def test_grading_not_over_limit(self):
        """Teste qu'une notation ne peut pas être au-dessus du maximum"""

        payload = {
            "grading": MAX_GRADING_VALUE + 1,
            "draft": False,
        }

        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotIn("id", res.data)

    def test_grading_not_under_limit(self):
        """Teste qu'une notation ne peut pas être au-dessous du minimum"""

        payload = {
            "grading": MIN_GRADING_VALUE - 1,
            "draft": False,
        }

        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotIn("id", res.data)

    def test_grading_not_float(self):
        """Teste qu'une notation ne peut pas être décimale"""

        payload = {
            "grading": 5.5,
            "draft": False,
        }

        res = self.client.post(self.fiction_reviews_url, payload)

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertNotIn("id", res.data)



def generate_reviewsonme_url(review_id):
    return reverse("app:reviewsonme:review-detail", args=[review_id])

def generate_reviewsonme_replies_url(review_id, review_reply_id):
    if review_reply_id:
        return reverse("app:reviewsonme:review-reply-detail", args=[review_id, review_reply_id])
    return reverse("app:reviewsonme:review-reply-list", args=[review_id])

def generate_myreviews_url(review_id):
    return reverse("app:myreviews:myreview-detail", args=[review_id])

def generate_myreviews_replies_url(review_id, review_reply_id):
    if review_reply_id:
        return reverse("app:myreviews:myreview-reply-detail", args=[review_id, review_reply_id])
    return reverse("app:myreviews:myreview-reply-list", args=[review_id])


class TestsReviewReplying(APITestCase):
    """Testent la création de réponses à reviews"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.fiction = sample_fiction(creation_user=cls.author)
        cls.reviewer = sample_user()
        cls.review = sample_review(creation_user=cls.reviewer, work=cls.fiction, draft=False)
        cls.client = APIClient()

    def test_author_replies_to_review(self):
        """Teste qu'un auteur peut répondre à une review le concernant"""

        payload = {
            "text": "Exemple de texte de ràr",
        }

        self.client.force_authenticate(self.author)

        res = self.client.post(generate_reviewsonme_url(self.review.id), payload)

        self.assertEqual(res.status_code, HTTP_201_CREATED)

    def test_reviewer_replies_to_review_reply(self):
        """Teste qu'un reviewer peut répondre à une ràr"""

        review_reply = ReviewReply.objects.create(
            creation_user=self.author,
            text="Exemple de texte de ràr",
            review=self.review,
        )

        payload = {
            "text": "Exemple de texte de rràr",
        }

        self.client.force_authenticate(self.reviewer)

        res = self.client.post(generate_myreviews_replies_url(self.review.id, review_reply_id=review_reply.id), data=payload)

        self.assertEqual(res.status_code, HTTP_201_CREATED)

    def test_author_replies_to_reply_to_review_reply(self):
        """Teste qu'un auteur peut répondre à une rràr"""

        review_reply = ReviewReply.objects.create(
            creation_user=self.author,
            text="Exemple de texte de ràr",
            review=self.review,
        )

        review_reply_reply = ReviewReply.objects.create(
            creation_user=self.reviewer,
            text="Exemple de texte de rràr",
            parent=review_reply,
        )

        payload = {
            "text": "Exemple de texte de rrràr",
        }

        self.client.force_authenticate(self.author)

        res = self.client.post(generate_reviewsonme_replies_url(self.review.id, review_reply_id=review_reply_reply.id),
                               data=payload)

        self.assertEqual(res.status_code, HTTP_201_CREATED)

    def tearDown(self) -> None:
        self.review.replies.all().delete()


class TestsReviewReplyValidation(APITestCase):
    """Testent la validation des réponses à reviews"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.fiction = sample_fiction(creation_user=cls.author)
        cls.reviewer = sample_user()
        cls.review = sample_review(creation_user=cls.reviewer, work=cls.fiction, draft=False)

        cls.client = APIClient()

    def test_review_reply_text_not_blank(self):
        """Teste que le texte d'une réponse à review ne peut pas être vide"""

        payload = {
            "text": "",
        }

        self.client.force_authenticate(self.author)

        res = self.client.post(generate_reviewsonme_url(self.review.id), payload)

        self.assertEqual(res.status_code, HTTP_400_BAD_REQUEST)
        self.assertIn("text", res.data)


class TestsReviewReplyingPermissions(APITestCase):
    """Testent les permissions des réponses à reviews"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.fiction = sample_fiction(creation_user=cls.author)
        cls.reviewer = sample_user()
        cls.review = sample_review(creation_user=cls.reviewer, work=cls.fiction, draft=False)
        cls.review_reply = ReviewReply.objects.create(
            creation_user=cls.author,
            text="Exemple de texte de ràr",
            review=cls.review,
        )

        cls.client = APIClient()

    def test_only_one_review_reply_per_author(self):
        """Teste qu'une seule réponse à review est possible par auteur"""

        payload = {
            "text": "Exemple de texte de ràr 2",
        }

        self.client.force_authenticate(self.author)

        res = self.client.post(generate_reviewsonme_url(self.review.id), payload)

        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

    def test_only_one_reply_to_review_reply(self):
        """Teste qu'une seule réponse à réponse à review est possible par reviewer"""

        ReviewReply.objects.create(
            creation_user=self.reviewer,
            text="Exemple de texte de rràr 1",
            parent=self.review_reply,
        )

        payload = {
            "text": "Exemple de texte de rràr 2",
        }

        self.client.force_authenticate(self.reviewer)

        res = self.client.post(generate_myreviews_replies_url(self.review.id, self.review_reply.id), data=payload)

        self.assertEqual(res.status_code, HTTP_403_FORBIDDEN)

    def tearDown(self) -> None:
        self.client.force_authenticate(None)
        self.review_reply.replies.all().delete()
