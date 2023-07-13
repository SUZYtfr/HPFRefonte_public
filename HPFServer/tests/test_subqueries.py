from django.test import TestCase, override_settings

from core.management.utils.samples import (
    sample_chapter,
)
from fictions.models import Fiction, Chapter
from fictions.enums import ChapterValidationStage


"""
Teste les sous-requêtes qui plantent tout le temps.

# TODO - Prendre en compte chapitres non publiés, reviews non publiées
# TODO - average
"""

@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}})
class TestSubqueries(TestCase):
    fixtures = [
        "fixtures/users.json",
        "fixtures/characteristics.json",
    ]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.sample_chapter_ids = []
        cls.sample_chapter_fiction_ids = []
        for x in range(10):
            chapter = sample_chapter(
                image_count=0,
                read_count=1000,
                validation_status=ChapterValidationStage.PUBLISHED,
            )
            cls.sample_chapter_ids.append(chapter.id)
            cls.sample_chapter_fiction_ids.append(chapter.fiction_id)
        cls.first_chapter_id = cls.sample_chapter_ids[0]
        cls.first_chapter_fiction_id = cls.sample_chapter_fiction_ids[0]

    def test_chapter_subqueries_correct(self) -> None:
        plain = (
            Chapter.objects
            .get(id=self.first_chapter_id)
        )

        with_word_counts = (
            Chapter.objects
            .with_word_counts()
            .get(id=self.first_chapter_id)
        )

        self.assertEqual(with_word_counts.word_count, plain.word_count)

    def test_fiction_subqueries_correct(self) -> None:
        plain = (
            Fiction.objects
            .get(id=self.first_chapter_fiction_id)
        )

        with_word_counts = (
            Fiction.objects
            .with_word_counts()
            .get(id=self.first_chapter_fiction_id)
        )

        with_read_counts = (
            Fiction.objects
            .with_read_counts()
            .get(id=self.first_chapter_fiction_id)
        )

        with_word_and_read_counts = (
            Fiction.objects
            .with_word_counts()
            .with_read_counts()
            .get(id=self.first_chapter_fiction_id)
        )

        self.assertEqual(with_read_counts.read_count, plain.read_count)
        self.assertEqual(with_word_counts.word_count, plain.word_count)
        self.assertEqual(with_word_and_read_counts.read_count, plain.read_count)
        self.assertEqual(with_word_and_read_counts.word_count, plain.word_count)
