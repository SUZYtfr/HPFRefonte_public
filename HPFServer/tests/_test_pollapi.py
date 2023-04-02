from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework import status

from django.core.exceptions import ValidationError
from django.utils import timezone

from tests.samples import *
from selections.models import Selection
from fictions.models import Chapter
from polls.models import Ballot
from app.settings import MAX_POLL_ANSWERS
from polls.serializers import ResultSerializer, PollQuestionSerializer

from random import shuffle


MYPOLLS_URL = reverse("app:mypolls:mypoll-list")
MYPOLLANSWERS_URL = reverse("app:mypolls:mypollanswer-list")

POLLS_URL = reverse("app:polls:poll-list")


def generate_poll_vote_url(poll_id):
    return reverse("app:polls:vote", args=[poll_id])


def generate_poll_results_url(poll_question_id):
    return reverse("app:polls:results", args=[poll_question_id])


# Les sondages de thème et sélection sont créés par les modérateurs via la page d'administration
class TestsChapterPollCreationAPI(APITestCase):
    """Testent le comportement de l'API de création de sondage de chapitre"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.chapter = sample_chapter(creation_user=cls.author)
        cls.client = APIClient()

    def setUp(self) -> None:
        self.client.force_authenticate(self.author)

    def test_chapter_must_be_published_before_poll_creation(self):
        """Teste que le chapitre doit avoir été publié avant de pouvoir ajouter un sondage"""

        self.chapter.validation_status = Chapter.ValidationStage.DRAFT
        self.chapter.save()

        payload = {
            "question_text": "Exemple de texte de question",
            "chapter": self.chapter.id,
        }

        res = self.client.post(MYPOLLS_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_another_poll_for_same_chapter(self):
        """Teste qu'un seul sondage peut être créé par chapitre"""

        payload = {
            "question_text": "Exemple de texte de question",
            "chapter": self.chapter.id,
        }

        self.client.post(MYPOLLS_URL, data=payload)
        res = self.client.post(MYPOLLS_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_two_answers_must_be_added_before_poll_appears(self):
        """Teste que deux réponses doivent être présente avant que le sondage soit pris en compte"""

        question = sample_poll_question(creation_user=self.author, chapter=self.chapter)

        payload = {
            "answer_text": "Exemple de texte de réponse",
            "poll_question": question.id,
        }

        res = self.client.post(MYPOLLANSWERS_URL, data=payload)

        question_serializer = PollQuestionSerializer(question)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(question_serializer.data, self.client.get(MYPOLLS_URL).data)
        self.assertNotIn(question_serializer.data, self.client.get(POLLS_URL).data)

    def test_max_answers(self):
        """Teste que l'utilisateur ne peut pas ajouter de réponses au-dessus du maximum autorisé"""

        question = sample_poll_question(creation_user=self.author, chapter=self.chapter)

        for x in range(MAX_POLL_ANSWERS):
            sample_poll_answer(poll_question=question)

        payload = {
            "answer_text": "Exemple de texte de réponse",
            "poll_question": question.id,
        }

        res = self.client.post(MYPOLLANSWERS_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self) -> None:
        self.chapter.validation_status = Chapter.ValidationStage.PUBLISHED
        self.chapter.save()
        if poll := self.chapter.poll:
            poll.delete()


class TestsPollVoteAPI(APITestCase):
    """Testent le comportement de l'API de vote"""

    @classmethod
    def setUpTestData(cls):
        cls.creator = sample_user()

        cls.simple_question = sample_poll_question(max_choices=1, creation_user=cls.creator)
        cls.simple_q_answer_1 = sample_poll_answer(poll_question=cls.simple_question)
        cls.simple_q_answer_2 = sample_poll_answer(poll_question=cls.simple_question)

        cls.qcm_question = sample_poll_question(max_choices=2, creation_user=cls.creator)
        cls.qcm_q_answer_1 = sample_poll_answer(poll_question=cls.qcm_question)
        cls.qcm_q_answer_2 = sample_poll_answer(poll_question=cls.qcm_question)

        cls.client = APIClient()
        cls.voter = sample_user()

    def setUp(self) -> None:
        self.client.force_authenticate(self.voter)

    def test_choices_not_empty(self):
        """Teste que le ballot doit contenir au moins un choix de réponse"""

        payload = {
            "choices": [],
        }

        res = self.client.post(generate_poll_vote_url(self.simple_question.id), data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_count_of_choices_of_answers_does_not_reach_over_maximum(self):
        """Teste que le maximum de choix de réponses par question ne peut pas être dépassé"""

        payload = {
            "choices": [
                self.simple_q_answer_1.id,
                self.simple_q_answer_2.id,
            ]
        }

        res = self.client.post(generate_poll_vote_url(self.simple_question.id), data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_id_must_belong_to_question_id(self):
        """Teste qu'un ID de réponse passé ne peut pas appartenir à une autre question"""

        payload = {
            "choices": [
                self.qcm_q_answer_1.id,
                self.simple_q_answer_1.id,
            ]
        }

        res = self.client.post(generate_poll_vote_url(self.qcm_question.id), data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_cannot_be_chosen_twice(self):
        """Teste qu'une réponse ne peut pas apparaître deux fois dans les choix"""

        payload = {
            "choices": [
                self.qcm_q_answer_1.id,
                self.qcm_q_answer_1.id,
            ]
        }

        res = self.client.post(generate_poll_vote_url(self.qcm_question.id), data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_or_ip_address_cannot_vote_twice(self):
        """Teste qu'un utilisateur / une adresse IP ne peut pas voter deux fois"""

        payload = {
            "choices": [
                self.simple_q_answer_1.id,
            ]
        }

        self.client.post(generate_poll_vote_url(self.simple_question.id), data=payload)

        with self.assertRaises(ValidationError):
            self.client.post(generate_poll_vote_url(self.simple_question.id), data=payload)

        # TODO - ajouter le test d'ip

    def test_all_answers_of_a_selection_poll_must_be_given(self):
        """Teste que toutes les réponses d'un sondage de sélection doivent être classées"""

        selection = Selection.objects.create(theme="Exemple de thème", description="Exemple de description", creation_user=self.creator)
        selection_question = sample_poll_question(selection=selection, creation_user=self.creator)
        selection_q_answers_id = [sample_poll_answer(poll_question=selection_question).id for x in range(3)]

        choices = selection_q_answers_id.copy()
        shuffle(choices)

        payload = {
            "choices": choices
        }

        res = self.client.post(generate_poll_vote_url(selection_question.id), data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_vote_outside_poll_datetime_boundaries(self):
        """Teste que le vote est rejeté avant la date d'ouverture et après la date de fermeture du sondage"""

        payload = {
            "choices": [
                self.simple_q_answer_1.id,
            ]
        }

        today = timezone.now()
        yesterday = today.replace(day=today.day - 1)
        tomorrow = today.replace(day=today.day + 1)

        self.simple_question.opening_datetime = tomorrow
        self.simple_question.save()

        res = self.client.post(generate_poll_vote_url(self.simple_question.id), data=payload)

        self.simple_question.opening_datetime = today
        self.simple_question.closing_datetime = yesterday
        self.simple_question.save()

        res2 = self.client.post(generate_poll_vote_url(self.simple_question.id), data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_members_only_poll(self):
        """Teste qu'un visiteur ne peut pas voter pour un sondage réservé aux membres"""

        self.simple_question.members_only = True
        self.simple_question.save()

        payload = {
            "choices": [
                self.simple_q_answer_1.id,
            ]
        }

        self.client.force_authenticate()

        res = self.client.post(generate_poll_vote_url(self.simple_question.id), data=payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self) -> None:
        Ballot.objects.filter(user=self.voter).delete()


class TestsPollResultsVisibility(APITestCase):
    """Testent la visibilité des résultats de sondage"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.chapter = sample_chapter(creation_user=cls.author)
        cls.simple_question = sample_poll_question(creation_user=cls.author, chapter=cls.chapter)
        cls.simple_q_answer_1 = sample_poll_answer(poll_question=cls.simple_question)
        cls.simple_q_answer_2 = sample_poll_answer(poll_question=cls.simple_question)
        cls.voter = sample_user()

        cls.client = APIClient()
        cls.simple_q_result_serializer = ResultSerializer(cls.simple_question)

    def test_results_visible_to_all_user(self):
        """Teste la visibilité des résultats non restreinte"""
        self.simple_question.members_only = False
        self.simple_question.visibility = True
        self.simple_question.save()

        res = self.client.get(generate_poll_results_url(poll_question_id=self.simple_question.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, self.simple_q_result_serializer.data)

    def test_results_visible_to_members_only(self):
        """Teste la visibilité des résultats restreinte aux membres"""
        self.simple_question.members_only = True
        self.simple_question.visibility = True
        self.simple_question.save()

        res = self.client.get(generate_poll_results_url(poll_question_id=self.simple_question.id))

        self.client.force_authenticate(self.voter)
        res2 = self.client.get(generate_poll_results_url(poll_question_id=self.simple_question.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertEqual(res2.data, self.simple_q_result_serializer.data)

    def test_results_visible_to_author_only(self):
        """Teste la visibilité des résultats restreinte à l'auteur"""
        self.simple_question.members_only = True
        self.simple_question.visibility = False
        self.simple_question.save()

        res = self.client.get(generate_poll_results_url(poll_question_id=self.simple_question.id))

        self.client.force_authenticate(self.voter)
        res2 = self.client.get(generate_poll_results_url(poll_question_id=self.simple_question.id))

        self.client.force_authenticate(self.author)
        res3 = self.client.get(generate_poll_results_url(poll_question_id=self.simple_question.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res2.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res3.status_code, status.HTTP_200_OK)
        self.assertEqual(res3.data, self.simple_q_result_serializer.data)
