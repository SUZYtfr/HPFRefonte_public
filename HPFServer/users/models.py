from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from core.models import DatedModel, ReviewableModel, FullCleanModel


class ActiveUserManager(models.Manager):
    """Gestionnaire d'utilisateurs actifs"""

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class UserManager(BaseUserManager):
    """Gestionnaire d'utilisateurs"""

    def create_user(self, nickname, email, birthdate, password, **extra_fields):
        """Crée un utilisateur"""

        user = self.model(
            nickname=nickname,
            email=self.normalize_email(email),
            birthdate=birthdate,
            is_active=True,
            **extra_fields)

        # Ceci est le moyen sûr de sauvegarder le mdp (cryptage)
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, nickname, email, password, **extra_fields):
        """Crée un super utilisateur"""

        if not nickname:
            raise ValueError("Le pseudonyme est obligatoire.")
        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")
        if not password:
            raise ValueError("Le mot de passe est obligatoire.")

        superuser = self.model(
            nickname=nickname,
            email=self.normalize_email(email),
            is_active=True,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )

        superuser.set_password(password)

        superuser.save_base()  # Échappe le full_clean()

        return superuser

    def create_anonymous_user(self, email, **extra_fields):
        """Crée un utilisateur anonyme"""

        if not email:
            raise ValueError("L'adresse e-mail est obligatoire.")

        anonymous_user = self.model(
            email=self.normalize_email(email),
            nickname=None,
            password=None,
            birthdate=None,
            is_active=False,
        )

        anonymous_user.save_base()  # Échappe le full_clean()

        return anonymous_user


class User(AbstractBaseUser, DatedModel, ReviewableModel, PermissionsMixin):
    """Modèle d'utilisateur"""

    class Meta:
        verbose_name = "utilisateur"
        permissions = [
            ("user_list_full_view", "Affiche la liste de tous les utilisateurs sur le site")
        ]

    class UserGender(models.IntegerChoices):
        UNDEFINED = (0, "Non renseigné")
        FEMALE = (1, "Femme")
        MALE = (2, "Homme")
        OTHER = (3, "Autre")

    # NOTE : nickname, password et birthdate laissé NULL pour les comptes anonymes
    # blank=False permet d'obliger l'UI à demander ces infos : seul le moteur peut créer des comptes anonymes
    nickname = models.CharField(max_length=200, verbose_name="pseudonyme",
                                unique=True, null=True, blank=False)
    realname = models.CharField(max_length=200, verbose_name="nom",
                                null=True, blank=True)
    email = models.EmailField(max_length=200, verbose_name="adresse e-mail",
                              unique=True)
    password = models.CharField(max_length=128, verbose_name="mot de passe",
                                null=True, blank=False)
    birthdate = models.DateField(verbose_name="date de naissance",
                                 null=True, blank=False)

    # Champs et préférences par défaut ultérieurement modifiables par l'utilisateur
    age_consent = models.BooleanField(verbose_name="accès au contenu +18 ans",
                                      default=False)
    bio = models.TextField(verbose_name="biographie",
                           null=False, blank=True, default="")
    gender = models.SmallIntegerField(verbose_name="genre",
                                      null=True, blank=True,
                                      choices=UserGender.choices)
    user_pref_font = models.CharField(max_length=50, verbose_name="préférence de police d'écriture",
                                      null=True, blank=True, default="Tahoma")
    user_pref_font_size = models.SmallIntegerField(verbose_name="préférence de taille de police",
                                                   null=True, blank=True, default=7.5)
    user_pref_line_spacing = models.DecimalField(verbose_name="préférence de taille d'interligne",
                                                 max_digits=3, decimal_places=2, default=1.0,
                                                 null=True, blank=True)
    user_pref_dark_mode = models.BooleanField(verbose_name="préférence de mode sombre",
                                              null=True, blank=True)
    user_pref_skin = models.CharField(max_length=50, verbose_name="préférence de thème",
                                      null=False, blank=True, default="default")
    user_pref_show_reaction = models.BooleanField(verbose_name="préférence d'affichage des réactions",
                                                  null=False, default=True)

    # Champs par défaut restreints modifiables par la modération
    is_beta = models.BooleanField(verbose_name="bêta",
                                  default=False)
    is_premium = models.BooleanField(verbose_name="adhérent",
                                     default=False)
    is_active = models.BooleanField(verbose_name="actif",
                                    default=True)

    # Champs par défaut restreints modifiables par l'administration
    is_staff = models.BooleanField(verbose_name="modérateur",
                                   default=False)
    is_superuser = models.BooleanField(verbose_name="administrateur",
                                       default=False)
    last_login = models.DateTimeField(verbose_name="dernière connexion",
                                      blank=True, null=True, editable=False)

    objects = UserManager()
    active = ActiveUserManager()

    # Il faut définir "à la main" quel champ est utilisé comme identifiant
    # La définition du champ "email" n'est pas nécessaire, mais on n'est jamais trop prudent
    # La définition de REQUIRED_FIELDS est nécessaire pour la création d'un superutilisateur via shell
    # nickname et password sont implicitement ajoutés à la liste
    USERNAME_FIELD = "nickname"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    @property
    def username(self):
        """Renvoie le pseudonyme ou [anonyme] si le compte est anonymisé"""

        return self.get_username() or "[anonyme]"

    def __str__(self):
        return self.username

    def remove_personal_information(self):
        """Supprime les informations personnelles de l'utilisateur"""
        self.nickname = None
        self.bio = ""
        self.birthdate = None
        self.gender = self.UserGender.UNDEFINED
        self.user_links.all().delete()
        try:
            self.banner.delete()
        except ObjectDoesNotExist:
            pass
        self.save_base()

    def delete_reviews(self):
        """Supprime les reviews de l'utilisateur"""
        for review in self.created_reviews.all():
            review.delete()

    def remove_authoring(self, anonymise=False):
        """Supprime l'autorat de l'utilisateur sur ses fictions

        Les fictions dont l'utilisateur est le seul auteur sont supprimées si indiqué."""
        for fiction in self.authored_fictions.all():
            fiction.authors.remove(self)
            if not anonymise and fiction.authors.count() == 0:
                fiction.delete()

    def ban(self, anonymise=False, keep_reviews=False):
        """Supprime les informations, reviews et fictions personnelles de l'utilisateur et le désactive"""

        self.remove_personal_information()
        if not keep_reviews:
            self.delete_reviews()
        self.remove_authoring(anonymise=anonymise)
        self.groups.clear()  # Supprime de tous les groupes / équipes
        self.is_staff = False
        self.is_superuser = False
        self.is_active = False
        self.modification_date = timezone.now()
        self.save_base()

    def save(self, *args, **kwargs):
        if not self.is_superuser and not self.is_anonymous:
            self.full_clean()
        super().save_base(*args, **kwargs)


class UserLink(FullCleanModel):
    """Modèle de lien de profil d'utilisateur"""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="user_links",
                             verbose_name="utilisateur")
    url = models.URLField(verbose_name="URL")
    display_text = models.CharField(max_length=50, verbose_name="texte du lien")

    class Meta:
        verbose_name = "lien externe"
        verbose_name_plural = "liens externes"

    def __str__(self):
        return "<a href='" + str(self.url) + "'>" + str(self.display_text) + "</a>"
