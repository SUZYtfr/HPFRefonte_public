from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist

from core.models import DatedModel, get_user_deleted_sentinel
from fictions.models import Fiction, Chapter, ChapterTextVersion
from colls.models import Collection
from images.models import ProfilePicture


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class UserManager(BaseUserManager):
    """Gestionnaire d'utilisateurs"""

    @transaction.atomic
    def create_user(self, nickname, email, password, **extra_fields):
        """Crée un utilisateur"""

        user = self.model(
            nickname=nickname,
            email=self.normalize_email(email),
            is_active=True,
        )
        user.set_password(password)
        user.save()
        UserProfile.objects.create(
            pk=user.pk,  # TODO - est-ce une bonnée idée ?
            **extra_fields,
        )
        UserPreferences.objects.create(
            pk=user.pk,  # TODO - est-ce une bonnée idée ?
        )

        return user

    def create_superuser(self, nickname, email, password, **extra_fields):
        """Crée un super utilisateur"""

        superuser = self.model(
            nickname=nickname,
            email=self.normalize_email(email),
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )

        superuser.set_password(password)

        superuser.save_base()

        return superuser

    def create_anonymous_user(self, email, **extra_fields):
        """Crée un utilisateur anonyme"""

        anonymous_user = self.model(
            email=self.normalize_email(email),
            nickname=None,
            is_active=False,
        )
        anonymous_user.set_unusable_password()
        anonymous_user.save()

        return anonymous_user

    def active(self):
        return UserQuerySet(self.model).active()


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle d'utilisateur"""

    class Meta:
        verbose_name = "utilisateur"
        permissions = [
            ("user_list_full_view", "Affiche la liste de tous les utilisateurs sur le site")
        ]

    # NOTE : nickname laissé NULL pour les comptes anonymes
    # blank=False permet d'obliger l'UI à demander ces infos : seul le moteur peut créer des comptes anonymes
    nickname = models.CharField(
        max_length=200,
        verbose_name="pseudonyme",
        unique=True,
        null=True,
        blank=False,
    )
    email = models.EmailField(
        max_length=200,
        verbose_name="adresse e-mail",
        unique=True,
        blank=False,
    )
    password = models.CharField(
        max_length=128,
        verbose_name="mot de passe",
        blank=False,
        # editable=False,
    )

    # Champs par défaut restreints modifiables par la modération
    is_beta = models.BooleanField(
        verbose_name="bêta",
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name="actif",
        default=True,
    )

    # Champs par défaut restreints modifiables par l'administration
    is_staff = models.BooleanField(
        verbose_name="modérateur",
        default=False,
    )
    is_superuser = models.BooleanField(
        verbose_name="administrateur",
        default=False,
    )
    first_seen = models.DateTimeField(
        verbose_name="première apparition",
        null=True,
        auto_now_add=True,
    )
    last_login = models.DateTimeField(
        verbose_name="dernière connexion",
        null=True,
        editable=False,
    )

    objects = UserManager()

    # Il faut définir "à la main" quel champ est utilisé comme identifiant
    # La définition du champ "email" n'est pas nécessaire, mais on n'est jamais trop prudent
    # La définition de REQUIRED_FIELDS est nécessaire pour la création d'un superutilisateur via shell
    # nickname et password sont implicitement ajoutés à la liste
    USERNAME_FIELD = "nickname"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    @property
    def profile(self):
        return getattr(self, "user_profile", None)

    @property
    def username(self) -> str:
        """Renvoie le pseudonyme ou [anonyme] si le compte est anonymisé"""

        return self.get_username() or "[anonyme]"

    def __str__(self):
        return self.username

    @property
    def read_count(self) -> int:
        return (
            self.created_chapters
            .published()
            .aggregate(models.Sum("read_count"))["read_count__sum"]
        ) or 0

    @property
    def word_count(self) -> int:
        last_version = ChapterTextVersion.objects.filter(chapter=models.OuterRef("pk")).order_by("-creation_date")
        word_count = models.Subquery(last_version.values('word_count')[:1])
        return (
            self.created_chapters
            .published()
            .annotate(word_count=word_count)
            .aggregate(models.Sum("word_count"))["word_count__sum"]
        ) or 0

    @property
    def fiction_count(self) -> int:
        return self.created_fictions.published().count()

    @property
    def chapter_count(self) -> int:
        return self.created_chapters.published().count()

    @property
    def review_count(self) -> int:
        return self.created_reviews.filter(draft=False).count()

    @property
    def comment_count(self) -> int:
        return self.created_newscomments.count()

    @property
    def collection_count(self) -> int:
        return self.created_collections.count()

    @property
    def review_reply_count(self) -> int:
        return self.created_reviewreplys.count()

    @transaction.atomic
    def ban(self, anonymise=False, keep_reviews=False):
        """Supprime les informations, reviews et fictions personnelles de l'utilisateur et le désactive"""

        if not keep_reviews:
            for review in self.created_reviews.all():
                review.delete()

        for fiction in self.authored_fictions.all():
            fiction.authors.remove(self)
            if not anonymise and fiction.authors.count() == 0:
                fiction.delete()

        try:
            self.banner.delete()
        except ObjectDoesNotExist:
            pass

        self.profile.delete()
        self.preferences.delete()

        self.groups.clear()  # Supprime de tous les groupes / équipes
        self.is_staff = False
        self.is_superuser = False
        self.nickname = None

        self.is_active = False
        self.set_unusable_password()

        self.save()


class UserProfileManager(models.Manager):
    def create(self, **fields):
        profile_picture_fields = fields.pop("profile_picture")
        user_profile = super().create(**fields)
        if profile_picture_fields:
            ProfilePicture.objects.create(
                user_profile=user_profile,
                creation_user=user_profile.user,
                **profile_picture_fields,
            )

        return user_profile


class UserProfile(DatedModel):  # TODO - renverser le O2O
    class Gender(models.IntegerChoices):
        UNDEFINED = (0, "Non renseigné")
        FEMALE = (1, "Femme")
        MALE = (2, "Homme")
        OTHER = (3, "Autre")

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur",
        related_name="user_profile",
        primary_key=True,
        editable=False,
    )
    modification_user = models.ForeignKey(
        to=User,
        verbose_name="modificateur",
        # related_name="modified_%(class)ss",
        related_name="+",
        on_delete=models.SET(get_user_deleted_sentinel),
        null=True,
        editable=False,
    )
    realname = models.CharField(
        max_length=200,
        verbose_name="nom",
        null=True,  # TODO - False
        blank=True,
    )
    birthdate = models.DateField(
        verbose_name="date de naissance",
        null=True,
        blank=True,
    )
    bio = models.TextField(
        verbose_name="biographie",
        null=False,
        blank=True,
        default="",
    )
    gender = models.SmallIntegerField(
        verbose_name="genre",
        choices=Gender.choices,
        default=Gender.UNDEFINED,
        blank=True,
    )

    objects = UserProfileManager()

    class Meta:
        verbose_name = "profil"


class UserPreferences(models.Model):  # TODO - renverser le O2O
    class ReviewPolicy(models.IntegerChoices):
        OFF = 0, "désactivé"
        WRITE_TEXT = 1, "écriture de review"
        SEE_TEXT = 2, "affichage de texte"  # + écriture
        WRITE_GRADING = 3, "notation de review"  # + écriture et visibilité
        SEE_GRADING = 4, "affichage de notation"  # + écriture et visibilité et notation

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur",
        related_name="preferences",
        primary_key=True,
    )
    age_consent = models.BooleanField(
        verbose_name="accès au contenu +18 ans",
        default=False,
    )
    font = models.CharField(
        max_length=50,
        verbose_name="police d'écriture",
        null=True,
        blank=True,
        default="Tahoma",
    )
    font_size = models.SmallIntegerField(
        verbose_name="taille de police",
        null=True,
        blank=True,
        default=7.5,
    )
    line_spacing = models.DecimalField(
        verbose_name="taille d'interligne",
        max_digits=3,
        decimal_places=2,
        default=1.0,
        null=True,
        blank=True,
    )
    dark_mode = models.BooleanField(
        verbose_name="mode sombre",
        null=True,
        blank=True,
    )
    skin = models.CharField(
        max_length=50,
        verbose_name="thème",
        null=False,
        blank=True,
        default="default",
    )
    show_reaction = models.BooleanField(
        verbose_name="affichage des réactions",
        null=False,
        default=True,
    )
    member_review_policy = models.SmallIntegerField(
        verbose_name="droits des membres",
        choices=ReviewPolicy.choices,
        default=ReviewPolicy.SEE_GRADING,
    )
    anonymous_review_policy = models.SmallIntegerField(
        verbose_name="droits des visiteurs",
        choices=ReviewPolicy.choices,
        default=ReviewPolicy.SEE_TEXT,
    )

    class Meta:
        verbose_name = "préférences d'utilisateur"
        verbose_name_plural = "préférences d'utilisateurs"
        constraints = [
            models.CheckConstraint(
                name="CK_users_userpreferences_anonymous_review_policy_lte_member_review_policy",
                check=models.Q(anonymous_review_policy__lte=models.F("member_review_policy")),
            ),
        ]


class UserLink(models.Model):
    """Modèle de lien de profil d'utilisateur"""

    user = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        related_name="user_links",
        verbose_name="utilisateur",
    )
    url = models.URLField(
        verbose_name="URL",
    )
    display_text = models.CharField(
        max_length=50,
        verbose_name="texte du lien",
    )

    class Meta:
        verbose_name = "lien externe"
        verbose_name_plural = "liens externes"

    def __str__(self):
        return "<a href='" + str(self.url) + "'>" + str(self.display_text) + "</a>"
