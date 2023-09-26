from decimal import Decimal

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction
from django.core.exceptions import ObjectDoesNotExist

from core.models import DatedModel, get_user_deleted_sentinel
from fictions.models import ChapterTextVersion
from images.models import ProfilePicture, Banner, ContentImage
from images.enums import BannerType
from .enums import (
    Gender,
    WebsiteType,
    ReviewPolicy,
    ColorScheme,
    Sort,
)


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class UserManager(BaseUserManager):
    """Gestionnaire d'utilisateurs"""

    @transaction.atomic
    def create_user(
        self,
        username,
        email,
        password,
        profile=None,
        preferences=None,
        **extra_fields
    ):
        """Crée un utilisateur"""

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            is_active=True,
            **extra_fields,
        )
        user.set_password(password)
        user.save()

        UserProfile.objects.create(
            pk=user.pk,  # TODO - est-ce une bonnée idée ?
            **(profile or {}),
        )
        UserPreferences.objects.create(
            pk=user.pk,  # TODO - est-ce une bonnée idée ?
            **(preferences or {}),
        )

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Crée un super utilisateur"""

        superuser = self.model(
            username=username,
            email=self.normalize_email(email),
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )

        superuser.set_password(password)

        superuser.save_base()

        return superuser

    def active(self):
        return UserQuerySet(self.model).active()


class User(AbstractBaseUser, PermissionsMixin):
    """Modèle d'utilisateur"""

    class Meta:
        verbose_name = "utilisateur·ice"
        verbose_name_plural = "utilisateur·ice·s"
        permissions = [
            ("user_list_full_view", "Affiche la liste de tous les utilisateurs sur le site")
        ]

    objects = UserManager()

    # NOTE : username laissé NULL pour les comptes anonymes
    # blank=False permet d'obliger l'UI à demander ces infos : seul le moteur peut créer des comptes anonymes
    username = models.CharField(
        max_length=200,
        verbose_name="pseudonyme",
        unique=True,
        null=False,
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
    is_active = models.BooleanField(
        verbose_name="actif",
        default=True,
    )
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
        editable=True,
    )

    # Il faut définir "à la main" quel champ est utilisé comme identifiant
    # La définition du champ "email" n'est pas nécessaire, mais on n'est jamais trop prudent
    # La définition de REQUIRED_FIELDS est nécessaire pour la création d'un superutilisateur via shell
    # username et password sont implicitement ajoutés à la liste
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    @property
    def profile(self):
        return getattr(self, "user_profile", None)

    @property
    def preferences(self):
        return getattr(self, "user_preferences", None)

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
        self.username = None

        self.is_active = False
        self.set_unusable_password()

        self.save()


class UserProfileManager(models.Manager):
    def create(
        self,
        profile_picture=None,
        banner=None,
        bio_images=None,
        **extra_fields,
    ):
        user_profile = super().create(**extra_fields)
        
        if profile_picture:
            user_profile.profile_picture = profile_picture
        
        if banner:
            user_profile.banner = banner

        if bio_images:
            images = [
                ContentImage(
                    **_hpf_image,
                    creation_user=user_profile.user,                
                ) for _hpf_image in bio_images
            ]
            ContentImage.objects.bulk_create(images)
            user_profile.bio_images.set(images)
            
        return user_profile


class UserProfile(DatedModel):  # TODO - renverser le O2O
    class Meta:
        verbose_name = "profil"
    
    objects = UserProfileManager()
    
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur",
        related_name="user_profile",
        primary_key=True,
        editable=True,
    )
    modification_user = models.ForeignKey(
        to=User,
        verbose_name="modificateur",
        # related_name="modified_%(class)ss",
        related_name="+",
        on_delete=models.SET(get_user_deleted_sentinel),
        null=True,
        editable=True,
    )
    realname = models.CharField(
        max_length=200,
        verbose_name="nom",
        null=True, 
        blank=True,
        default="",
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
    bio_images = models.ManyToManyField(
        verbose_name="images de biographie",
        to="images.ContentImage",
        related_name="profile",
    )
    gender = models.SmallIntegerField(
        verbose_name="genre",
        choices=Gender.choices,
        default=Gender.UNDEFINED,
        blank=True,
    )
    website = models.URLField(
        verbose_name="site perso",
        null=False,
        blank=True,
        default="",
    )
    age_consent = models.BooleanField(
        verbose_name="accès au contenu +18 ans",
        default=False,
    )

    def __str__(self) -> str:
        return f"Profil de {str(self.user)}"

    @property
    def profile_picture(self):
        return getattr(self, "user_profile_picture", None)

    @profile_picture.setter
    def profile_picture(self, profile_picture):
        if current_profile_picture := self.profile_picture:
            current_profile_picture.delete()
        ProfilePicture.objects.create(
            user_profile=self,
            creation_user=self.user,
            display_height=0,  # FIXME - supprimer les dimensions du modèle d'avatar
            display_width=0,
            is_adult_only=False,
            is_user_property=True,
            **profile_picture,
        )        

    @property
    def banner(self):
        return getattr(self, "user_banner", None)
    
    @banner.setter
    def banner(self, banner):
        if current_banner := getattr(self, "banner", None):
            current_banner.delete()
        Banner.objects.create(
            user_profile=self,
            creation_user=self.user,
            display_height=0,  # FIXME - supprimer les dimensions du modèle de bannière
            display_width=0,
            category=BannerType.PREMIUM,
            **banner,
        )


class UserPreferences(models.Model):  # TODO - renverser le O2O  
    class Meta:
        verbose_name = "préférences"
        verbose_name_plural = "préférences"
        constraints = [
            models.CheckConstraint(
                name="CK_%(app_label)s_%(class)s_anonymous_review_policy_lte_member_review_policy",
                check=models.Q(anonymous_review_policy__lte=models.F("member_review_policy")),
            ),
        ]

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="utilisateur",
        related_name="user_preferences",
        primary_key=True,
        editable=True,
    )

    # APPARENCE
    skin = models.CharField(
        max_length=50,
        verbose_name="thème",
        # null=False,
        # blank=True,
        default="default",
    )
    color_scheme = models.PositiveSmallIntegerField(
        verbose_name="mode d'affichage",
        choices=ColorScheme.choices,
        default=ColorScheme.AUTO,
    )
    color_scheme_in_reader = models.BooleanField(
        verbose_name="mode d'affichage dans le lecteur",
        choices=ColorScheme.choices,
        default=ColorScheme.AUTO,
    )
    show_animations = models.BooleanField(
        verbose_name="jouer les animations",
        default=True,
    )
    show_profile_pictures = models.BooleanField(
        verbose_name="afficher les avatars",
        default=True,
    )

    # LECTURE / ACCESSIBILITÉ
    font = models.CharField(
        verbose_name="police d'écriture",
        max_length=50,
        null=True,
        blank=True,
    )
    font_size = models.PositiveSmallIntegerField(
        verbose_name="taille de police",
        default=100,
        help_text="Taille de la police d'écriture en pourcentage de la taille d'origine."
    )
    line_spacing = models.DecimalField(
        verbose_name="taille d'interligne",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        default=Decimal(1.0),
    )
    letter_spacing = models.DecimalField(
        verbose_name="taille d'interlettre",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        default=Decimal(1.0),
    )
    paragraph_spacing = models.DecimalField(
        verbose_name="taille d'inter-paragraphe",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        default=Decimal(1.0),
    )
    redirect_to_summary = models.BooleanField(
        verbose_name="rediriger vers la table des matières",
        default=True,
        help_text="Indique si cliquer sur le titre d'une fiction ouvre la page de fiction ou de premier chapitre.",
    )
    show_trigger_warnings = models.BooleanField(
        verbose_name="afficher les avertissements",
        default=True,
        help_text="Indique si les avertissements doivent être affichés en début de chapitre.",
    )
    show_review_editor = models.BooleanField(
        verbose_name="afficher l'éditeur de reviews",
        default=True,
        help_text="Indique si l'éditeur de reviews doit être affiché par défaut dans le lecteur.",
    )
    # show_reaction = models.BooleanField(
    #     verbose_name="affichage des réactions",
    #     null=False,
    #     default=True,
    # )

    # NOTIFICATIONS
    email_for_review = models.BooleanField(
        verbose_name="nouvelle review",
        default=True,
    )
    email_for_reply = models.BooleanField(
        verbose_name="nouvelle réponse",
        default=True,
    )
    email_for_news = models.BooleanField(
        verbose_name="nouvelle news",
        default=True,
    )
    email_for_favorite_activity = models.BooleanField(
        verbose_name="nouveau favori",
        default=True,
    )
    email_for_favorite = models.BooleanField(
        verbose_name="nouvelle mise en favoris",
        default=True,
    )
    email_for_chapter_status = models.BooleanField(
        verbose_name="changement de statut de publication",
        default=True,
    )

    # ACCÈS ET DROITS DE REVIEWS
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

    # RECHERCHE
    result_order = models.PositiveSmallIntegerField(
        verbose_name="ordre de tri",
        choices=Sort.choices,
        default=Sort.ALPHA_ASC,
    )

    def __str__(self) -> str:
        return f"Préférences de {str(self.user)}"


class ExternalProfile(models.Model):
    """Modèle de lien de profil d'utilisateur externe"""

    class Meta:
        verbose_name = "profil externe"
        verbose_name_plural = "profils externes"

    user_profile = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        related_name="external_profiles",
        verbose_name="profil",
    )
    website_type = models.SmallIntegerField(
        verbose_name="type de site web",
        choices=WebsiteType.choices,
    )
    username = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        default="",
        verbose_name="pseudonyme",
    )
    is_visible = models.BooleanField(
        default=True,
        verbose_name="visible",
    )

    def __str__(self):
        return f"{self.external_username} sur {str(self.website_type)}"
  