from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from rest_framework import status
from rest_framework.reverse import reverse

from tests.samples import *
from fictions.models import Chapter, Beta
from fictions.serializers import BetaSerializer


def generate_beta_url(beta_id=None):
    if beta_id:
        return reverse("app:betas:beta-detail", args=[beta_id])
    else:
        return reverse("app:betas:beta-list")


class TestsBetaActions(APITestCase):
    """Testent les actions de bêtatage"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.author = sample_user()
        cls.beta_user = sample_user()
        cls.chapter = sample_chapter(
            creation_user=cls.author,
            text=lorem.get_paragraph(),
        )

    def test_beta_accept_changes_chapter_status_to_beta_ongoing(self):
        """Teste que l'acceptation du bêtatage par le correcteur modifie le statut du chapitre"""
        beta = Beta.objects.create(
            chapter=self.chapter,
            user=self.beta_user,
        )

        self.client.force_authenticate(self.beta_user)

        res = self.client.put(
            path=generate_beta_url(beta_id=beta.id),
            data={
                "stage": Beta.BetaStage.ONGOING.value,
            }
        )

        self.chapter.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.chapter.validation_status, Chapter.ValidationStage.BETA_ONGOING.value)

    def test_beta_complete_changes_chapter_status_to_beta_complete(self):
        """Teste que la complétion du bêtatage par l'auteur modifie le statut du chapitre"""
        beta = Beta.objects.create(
            chapter=self.chapter,
            user=self.beta_user,
            stage=Beta.BetaStage.CORRECTED,
        )

        self.client.force_authenticate(self.author)

        res = self.client.put(
            path=generate_beta_url(beta_id=beta.id),
            data={
                "stage": Beta.BetaStage.COMPLETED.value,
                "text": self.chapter.text,
            }
        )

        self.chapter.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.chapter.validation_status, Chapter.ValidationStage.BETA_COMPLETE.value)

    def test_saved_text_version_during_beta_updates_chapter_wordcount(self):
        """Teste que le compte de mot du chapitre est mis à jour à la sauvegarde d'une nouvelle version du texte"""
        beta = Beta.objects.create(
            chapter=self.chapter,
            user=self.beta_user,
            stage=Beta.BetaStage.ONGOING,
        )

        self.client.force_authenticate(self.beta_user)

        old_count = self.chapter.word_count
        new_text = self.chapter.text + lorem.get_word()

        res = self.client.put(
            path=generate_beta_url(beta_id=beta.id),
            data={
                "stage": Beta.BetaStage.ONGOING.value,
                "text": new_text,
            }
        )

        self.chapter.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.chapter.word_count, old_count)

    def tearDown(self) -> None:
        self.chapter.betas.all().delete()


class TestsBetaSerializers(APITestCase):
    """Testent les informations des sérialiseurs de bêtatage"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.factory = APIRequestFactory()
        cls.request = cls.factory.get("/")

        cls.author = sample_user()
        cls.beta_user = sample_user()
        cls.chapter = sample_chapter(
            creation_user=cls.author,
            text=lorem.get_paragraph(),
        )

    # TODO - ce test est mal fichu, tout comme le suivant, on devrait pouvoir trouver un moyen
    # de tester le formulaire auto-généré par les sérialiseurs avec le contexte passé, pas la réponse
    def test_chapter_text_not_editable_in_request_stage(self):
        """Teste que le texte n'est pas modifiable à l'étape de demande de bêtatage"""

        beta = Beta.objects.create(
            chapter=self.chapter,
            user=self.beta_user,
        )

        self.client.force_authenticate(self.beta_user)

        res = self.client.put(
            path=generate_beta_url(beta_id=beta.id),
            data={
                "stage": Beta.BetaStage.REFUSED.value,
                "text": "Exemple de texte impromptu",
            }
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # TODO - chaud de passer le contexte au sérialiseur, à corriger dès que je comprends le blème...
    def test_published_chapters_or_with_beta_ongoing_not_in_chapter_choices(self):
        """Teste que la liste des chapitres candidats au bêtatage n'inclut pas les chapitres en bêtatage ou publiés"""

        fac = APIRequestFactory()
        force_authenticate(self.author)
        request = fac.post(generate_beta_url())
        context = {"request": request}

        beta_ongoing_chapter = sample_chapter(
            creation_user=self.author,
            validation_status=Chapter.ValidationStage.BETA_ONGOING,
        )

        published_chapter = sample_chapter(
            creation_user=self.author,
            validation_status=Chapter.ValidationStage.PUBLISHED,
        )

        self.client.force_authenticate(self.author)

        beta_creation_feature_choices = []
        [beta_creation_feature_choices.extend(list(value.keys()))
         for value in BetaSerializer(context=context).get_fields().get("chapter").choices.values()]

        self.assertNotIn(published_chapter.id, beta_creation_feature_choices)
        self.assertNotIn(beta_ongoing_chapter.id, beta_creation_feature_choices)
        self.assertIn(self.chapter.id, beta_creation_feature_choices)


class TestsBetaViews(APITestCase):
    """Testent les accès aux bêtatages"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.author = sample_user()
        cls.beta_user = sample_user()
        cls.fiction = sample_fiction(
            creation_user=cls.author,
            generate_chapters=3,
        )

    def test_beta_list_does_not_contain_closed_betas(self):
        """Teste que les bêtatages clos (refusés et complétés) ne sont pas dans les listes de bêtatage"""

        active_beta = Beta.objects.create(
            chapter=self.fiction.chapters.all()[0],
            user=self.beta_user,
            stage=Beta.BetaStage.ONGOING,
        )
        refused_beta = Beta.objects.create(
            chapter=self.fiction.chapters.all()[1],
            user=self.beta_user,
            stage=Beta.BetaStage.REFUSED,
        )
        completed_beta = Beta.objects.create(
            chapter=self.fiction.chapters.all()[2],
            user=self.beta_user,
            stage=Beta.BetaStage.COMPLETED,
        )

        self.client.force_authenticate(self.author)
        res1 = self.client.get(generate_beta_url())

        self.client.force_authenticate(self.beta_user)
        res2 = self.client.get(generate_beta_url())

        self.assertIn(BetaSerializer(active_beta).data, res1.data)
        self.assertNotIn(BetaSerializer(refused_beta).data, res1.data)
        self.assertNotIn(BetaSerializer(completed_beta).data, res1.data)

        self.assertIn(BetaSerializer(active_beta).data, res2.data)
        self.assertNotIn(BetaSerializer(refused_beta).data, res2.data)
        self.assertNotIn(BetaSerializer(completed_beta).data, res2.data)
