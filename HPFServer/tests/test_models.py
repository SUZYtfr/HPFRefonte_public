from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.files.images import ImageFile

from .samples import *

from datetime import date
import tempfile
from PIL import Image
from pathlib import Path

from users.models import User
from fictions.models import Fiction, Chapter
from features.models import Category, Feature
from selections.models import Selection, Proposition
from reviews.models import Review, ReviewReply, MIN_GRADING_VALUE, MAX_GRADING_VALUE
from banners.models import Banner, validate_maximum_size


class TestCoreModels(TestCase):
    """Testent les modèles de base"""

    def test_creation_of_dated_model_through_user_model(self):
        """Teste la création d'un modèle de base d'horodatage de création / modification par le biais du modèle User"""
        user = sample_user()
        self.assertEqual(user.creation_date.date(), date.today())

    def test_creation_of_created_model_through_characteristic_model(self):
        """Teste la création d'un modèle de base de créateur / modificateur par le biais du modèle Feature"""
        user = sample_user()
        feature = sample_feature(creation_user=user)

        self.assertEqual(feature.creation_user, user)
        self.assertEqual(feature.modification_user, None)
        self.assertIn(feature, user.created_features.all())

    def test_creation_of_authored_model_through_fiction_model(self):
        """Teste la création d'un modèle de base d'autorat par le biais du modèle Fiction"""
        author = sample_user()
        fiction = sample_fiction(creation_user=author)

        self.assertIn(author, fiction.authors.all())
        self.assertIn(fiction, author.authored_fictions.all())


class TestsAllModels(TestCase):
    """Tests communs portant sur tous les modèles"""

    def test_str_values_of_models(self):
        """Teste la valeur de chaîne des différents objets"""
        nickname = "Michou"
        user = sample_user(nickname=nickname)
        fiction_title = "Exemple de titre de fiction"
        fiction = sample_fiction(creation_user=user, title=fiction_title)
        chapter_title = "Exemple de titre de chapitre"
        chapter = sample_chapter(creation_user=user, title=chapter_title, fiction=fiction)
        collection_title = "Exemple de titre de série"
        collection = sample_collection(creation_user=user, title=collection_title)
        feature_name = "Exemple de nom caractéristique"
        feature = sample_feature(creation_user=user, name=feature_name)
        category = random_category()

        self.assertEqual(str(user), nickname)
        self.assertEqual(str(fiction), fiction_title)
        self.assertEqual(str(chapter), chapter_title)
        self.assertEqual(str(collection), collection_title)
        self.assertEqual(str(category), category.name)
        self.assertEqual(str(feature), feature_name)


class TestsUserModel(TestCase):
    """Testent le modèle d'utilisateur"""

    def test_create_user_with_basic_required_info(self):
        """Teste la création d'un utilisateur avec les infos de base"""
        nickname = "Michou"
        email = "michel@salut.fr"
        password = "MotDePasse123"
        birthdate = "1988-05-12"

        user = User.objects.create_user(
            nickname=nickname,
            email=email,
            password=password,
            birthdate=birthdate
        )

        self.assertEqual(str(user), user.nickname)
        self.assertNotEqual(user.password, password)  # mot de passe est crypté
        self.assertTrue(user.check_password(password))  # mot de passe est correct
        self.assertEqual(user.is_active, True)

    def test_email_address_normalized(self):
        """Teste que l'adresse e-mail est normalisée à l'enregistrement"""
        email_domain_name_in_caps = "michel@SALUT.fr"
        user = sample_user(email=email_domain_name_in_caps)

        self.assertEqual(user.email, email_domain_name_in_caps.lower())

    def test_create_superuser(self):
        """Teste la création d'un superutilisateur (admin)"""
        superuser = User.objects.create_superuser(
            nickname="Paulo Modulo",
            email="paulo@modulo.fr",
            password="PassPauLo123"
        )

        self.assertEqual(superuser.is_active, True)
        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(superuser.is_superuser, True)

    def test_user_ban(self):
        """Teste le bannissement / la suppression d'un compte"""
        user = sample_user(
            bio=lorem.get_paragraph(),
            realname=lorem.get_word(),
            gender=User.UserGender.OTHER,
            birthdate=timezone.now())
        fiction = sample_fiction(creation_user=user)
        chapter = sample_chapter(creation_user=user)
        review = sample_review(creation_user=user)

        user.ban(anonymise=False, keep_reviews=False)

        self.assertEqual(user.bio, "")
        self.assertFalse(user.is_active)
        self.assertEqual(user.gender, User.UserGender.UNDEFINED)
        self.assertIsNone(user.nickname)
        self.assertIsNone(user.birthdate)
        with self.assertRaises(Fiction.DoesNotExist):
            fiction.refresh_from_db()
        with self.assertRaises(Chapter.DoesNotExist):
            chapter.refresh_from_db()
        with self.assertRaises(Review.DoesNotExist):
            review.refresh_from_db()

    def test_reviews_and_fictions_anonymised(self):
        """Teste que les fictions et reviews sont anonymisées si indiqué"""
        user = sample_user()

        fiction = sample_fiction(creation_user=user)
        review = sample_review(creation_user=user)

        user.ban(anonymise=True, keep_reviews=True)

        self.assertIsNone(fiction.refresh_from_db())
        self.assertEqual(fiction.authors.count(), 0)
        self.assertIsNone(review.refresh_from_db())

    def test_fictions_persistence(self):
        """Teste que les fictions persistent si elles sont co-autorées"""
        user = sample_user()
        user_2 = sample_user()

        fiction = sample_fiction(creation_user=user)
        fiction.authors.add(user_2)

        user.ban(anonymise=False)

        self.assertIsNone(fiction.refresh_from_db())
        self.assertNotIn(user, fiction.authors.all())


class TestsFictionModel(TestCase):
    """Testent le modèle de fiction"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()

    def test_fiction_word_count(self):
        """Teste que le compte de mots d'une fiction correspond à la somme de ceux de ses chapitres validés"""

        fiction = sample_fiction(creation_user=self.author)
        validated_chapter_1 = sample_chapter(
            creation_user=self.author,
            fiction=fiction,
            validation_status=Chapter.ChapterValidationStage.PUBLISHED,
        )
        validated_chapter_1.create_text_version(
            creation_user=self.author,
            text=lorem.get_paragraph(),
        )
        unvalidated_chapter_2 = sample_chapter(
            creation_user=self.author,
            fiction=fiction,
            validation_status=Chapter.ChapterValidationStage.DRAFT,
        )
        unvalidated_chapter_2.create_text_version(
            creation_user=self.author,
            text=lorem.get_paragraph(),
        )
        validated_chapter_3 = sample_chapter(
            creation_user=self.author,
            fiction=fiction,
            validation_status=Chapter.ChapterValidationStage.PUBLISHED,
        )
        validated_chapter_3.create_text_version(
            creation_user=self.author,
            text=lorem.get_paragraph(),
        )

        self.assertNotEqual(fiction.word_count, 0)
        self.assertEqual(fiction.word_count, sum([validated_chapter_1.word_count, validated_chapter_3.word_count]))

    def test_fiction_published_status(self):
        """Teste qu'une fiction est publique quand au moins un chapitre est validé"""
        unpublished_fiction = sample_fiction(creation_user=self.author, generate_chapters=1)
        published_fiction = sample_fiction(creation_user=self.author, generate_chapters=2)
        first_chapter = published_fiction.chapters.first()
        first_chapter.validation_status = 7
        first_chapter.save()

        unpublished_fiction.refresh_from_db()
        published_fiction.refresh_from_db()

        self.assertEqual(unpublished_fiction.is_published, False)
        self.assertEqual(published_fiction.is_published, True)


class TestFeatureModels(TestCase):
    """Testent les modèles de catégorie et de caractéristique"""

    @classmethod
    def setUpTestData(cls):
        cls.staff_user = sample_user(is_staff=True)

    def test_min_not_over_max_constraint(self):
        """Teste que le minimum de caractéristiques pour une catégorie ne peut pas être plus grand que le maximum"""

        with self.assertRaises(IntegrityError):
            Category.objects.create(
                creation_user=self.staff_user,
                name="Test catégorie minimum / maximum",
                is_closed=True,
                max_limit=2,
                min_limit=3,
            )

    def test_forbidden_features_are_removed_from_fiction_features(self):
        """Teste qu'une caractéristique interdite est retirée de la liste de caractéristique d'une fiction"""

        fiction = sample_fiction()
        replaced_feature = sample_feature()
        replacement_feature = sample_feature()
        forbidden_feature = sample_feature()

        fiction.features.set([replaced_feature, forbidden_feature])
        replaced_feature.ban(modification_user=self.staff_user, replace_with=replacement_feature)
        forbidden_feature.ban(modification_user=self.staff_user)

        self.assertNotIn(replaced_feature, fiction.features.all())
        self.assertNotIn(forbidden_feature, fiction.features.all())
        self.assertIn(replacement_feature, fiction.features.all())


class TestsSelectionModels(TestCase):
    """Testent les modèles de sélection et de propositions"""

    @classmethod
    def setUpTestData(cls):
        cls.user = sample_user()
        cls.staff_user = sample_user(is_staff=True)
        cls.fiction = sample_fiction()
        cls.open_selection = Selection.objects.create(
            creation_user=cls.user,
            theme="Exemple de thème",
            description="Exemple de description",
            open=True,
        )

    def setUp(self) -> None:
        self.open_selection.open = True
        self.open_selection.save()

    def test_only_one_selection_open(self):
        """Teste qu'une seule sélection peut être ouverte à la fois"""

        with self.assertRaises(IntegrityError):
            Selection.objects.create(
                creation_user=self.user,
                theme="Exemple de thème 2",
                description="Exemple de description 2",
                open=True,
            )

    def test_proposition_decision_info_not_mandatory_at_creation(self):
        """Teste que les informations de décision sur une proposition ne sont pas nécessaires à la création"""

        proposition = Proposition.objects.create(
            selection=self.open_selection,
            fiction=self.fiction,
            proposed_by=self.user,
        )

        self.assertIn(proposition, self.open_selection.propositions.all())

    def test_proposition_decision_info_mandatory_at_editing(self):
        """Teste que les informations de décision sur une proposition sont nécessaire à la modification"""

        proposition = Proposition.objects.create(
            selection=self.open_selection,
            fiction=self.fiction,
            proposed_by=self.user,
        )

        with self.assertRaises(ValidationError):
            proposition.save()

    def test_fiction_can_only_be_proposed_once_per_selection(self):
        """Teste qu'une fiction ne peut être proposée qu'une seule fois par sélection"""

        proposition = Proposition.objects.create(
            selection=self.open_selection,
            fiction=self.fiction,
            proposed_by=self.user,
        )

        proposition.decision = True
        proposition.decided_by = self.staff_user
        proposition.comment = "Exemple de commentaire de décision"
        proposition.save()

        with self.assertRaises(ValidationError):
            Proposition.objects.create(
                selection=self.open_selection,
                fiction=self.fiction,
                proposed_by=self.user,
            )

    def test_cannot_add_proposition_to_closed_selection(self):
        """Teste que les sélections fermées n'acceptent pas de propositions"""
        self.open_selection.open = False
        self.open_selection.save()

        with self.assertRaises(ValidationError):
            Proposition.objects.create(
                selection=self.open_selection,
                fiction=self.fiction,
                proposed_by=self.user,
            )

    @classmethod
    def tearDownClass(cls):
        cls.open_selection.delete()
        super().tearDownClass()


# NOTE : Il s'agit du même processus pour les reviews sur fictions, chapitres, séries et auteurs
class TestsReviewModels(TestCase):
    """Testent les modèles de reviews et de réponses à reviews"""

    @classmethod
    def setUpTestData(cls):
        cls.author = sample_user()
        cls.fiction = sample_fiction(cls.author)
        cls.review = sample_review(work=cls.fiction)
        cls.reviewer = sample_user()

    def test_grading_validators(self):
        """Teste les validateurs de notation"""
        with self.assertRaises(ValueError):
            sample_review(creation_user=self.reviewer, grading=MIN_GRADING_VALUE - 1)
        with self.assertRaises(ValueError):
            sample_review(creation_user=self.reviewer, grading=MAX_GRADING_VALUE + 1)
        with self.assertRaises(ValueError):
            sample_review(creation_user=self.reviewer, grading=5.2)

    def test_authors_cannot_review_themselves(self):
        """Teste qu'un auteur ne peut pas se reviewer lui-même ou ses œuvres"""
        with self.assertRaises(PermissionError):
            Review.objects.create(
                creation_user=self.author,
                work=self.fiction,
                text="Exemple de review",
            )

        with self.assertRaises(PermissionError):
            Review.objects.create(
                creation_user=self.author,
                work=self.author,
                text="Exemple de review",
            )

    def test_reviewer_can_only_review_once_per_object(self):
        """Teste qu'une seule review peut être écrite par reviewer et par objet"""
        sample_review(creation_user=self.reviewer, work=self.fiction)

        with self.assertRaises(PermissionError):
            sample_review(creation_user=self.reviewer, work=self.fiction)

    def test_only_authors_can_reply_to_review(self):
        """Teste que seul un auteur peut répondre à la review concernant son œuvre"""
        with self.assertRaises(PermissionError):
            ReviewReply.objects.create(
                creation_user=sample_user(),
                text=lorem.get_paragraph(),
                review=self.review,
            )

        with self.assertRaises(PermissionError):
            ReviewReply.objects.create(
                creation_user=sample_user(),
                text=lorem.get_paragraph(),
                review=sample_review(work=self.author))

    def test_only_one_reply_to_fiction_per_author(self):
        """Teste qu'une seule réponse est possible par auteur"""
        # RàR 1
        ReviewReply.objects.create(
            creation_user=self.author,
            text=lorem.get_paragraph(),
            review=self.review,
        )

        # RàR2
        with self.assertRaises(PermissionError):
            ReviewReply.objects.create(
                creation_user=self.author,
                text=lorem.get_paragraph(),
                review=self.review,
            )

    # devrait être automatique, en cascade, cf notes
    def test_deleting_review_with_a_reply(self):
        """Teste la suppression d'une review avec une réponse à review"""
        review = sample_review(creation_user=self.reviewer, work=self.fiction)
        ReviewReply.objects.create(creation_user=self.author, text="test", review=review)

        review.delete()

        self.assertEqual(self.author.created_reviewreplys.count(), 0)


class TestsBannerModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = sample_user()

        cls.ntf = tempfile.NamedTemporaryFile(suffix=".jpg")
        img = Image.new("RGB", (468, 10))
        img.save(cls.ntf, format="JPEG")
        cls.ntf.seek(0)

        cls.valid_banner_image = ImageFile(cls.ntf.file, name="test_banner.jpg")

    def test_banner_image_size_validator(self):
        """Teste le validateur de dimensions de l'image de bannière"""

        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (470, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)

            with ImageFile(ntf.file) as file:
                with self.assertRaises(ValidationError):
                    validate_maximum_size(file)

    def test_deleting_banner(self):
        """Teste la suppression de l'image de bannière du système de fichier lors de la suppression de la bannière"""

        banner = Banner.objects.create(
            creation_user=self.user,
            category=Banner.BannerType.WEBSITE,
            image=self.valid_banner_image,
        )
        file_path = Path(banner.image.path)

        file_exists = file_path.exists()

        banner.delete()

        file_still_exists = file_path.exists()

        self.assertTrue(file_exists)
        self.assertFalse(file_still_exists)

    @classmethod
    def tearDownClass(cls):
        cls.ntf.close()
        cls.valid_banner_image.close()
        super().tearDownClass()
