from django.test import TestCase, override_settings
from django.core.files.storage import default_storage

from core.management.utils.samples import sample_user


"""
Teste le système de fichiers.
Rappel : Le système de fichiers est en mémoire pour les tests. Ces tests portent sur
les interactions du serveur et d'un système du fichiers abstrait, et ne garantissent donc
pas le bon fonctionnement du système de fichiers de production !
"""

@override_settings(STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"}})
class TestFileSystem(TestCase):
    def test_profile_picture_lifecycle(self) -> None:
        user = sample_user(with_profile_picture=True)
        file_path = user.profile.profile_picture.src_path.path
        self.assertTrue(default_storage.exists(file_path))

        user.profile.profile_picture.delete()
        self.assertFalse(default_storage.exists(file_path))
