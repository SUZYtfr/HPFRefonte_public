from django.core.management.utils import get_random_secret_key
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('SECRET_KEY') or get_random_secret_key()

DEBUG = os.getenv("DEBUG", "1") == "1"  # astuce pour "parser" un boolean d'.env

ALLOWED_HOSTS = [os.getenv("SERVER_HOST", "*")]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000/",
# ]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "mptt",
    "polymorphic_tree",
    "strawberry_django",
    "ordered_model",
    "django_extensions",
    "django_filters",
    "core",
    "users",
    "account",
    "characteristics",
    "fictions",
    "reviews",
    "news",
    "images",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "strawberry_django_extras.jwt.middleware.jwt_middleware",
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "strawberry_django_extras.jwt.backend.JWTBackend",
]


'''
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
}
'''

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        'NAME': os.getenv("DB_NAME", BASE_DIR / "db.sqlite3"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'HOST': os.getenv("DB_HOST"),
        'PORT': os.getenv("DB_PORT"),
    },
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    "asyncio": {
        "handlers": None,
    },
}

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

MEDIA_ROOT = os.getenv("MEDIA_ROOT", BASE_DIR / 'media/')
STATIC_ROOT = os.getenv("STATIC_ROOT", BASE_DIR / "static/")

AUTH_USER_MODEL = 'users.User'

FIXTURE_DIRS = [
    BASE_DIR / "fixtures",
]

# HARDCODAGE
MODERATION_ACCOUNT = {
    "pk": 0,
    "username": "La modération",
    "email": "moderation@hpf.fr",
}
ANONYMOUS_ACCOUNT = {
    "pk": -1,
    "username": "",
    "email": "anonyme@hpf.fr",
}
# TODO faire des trigger warnings une table à part
TW_CHARTYPE_ID = 4

BANNER_MAX_SIZE = (468, 60)  # (largeur, hauteur)
MEMBERS_MAX_REVIEW_DRAFTS = 2
PREMIUM_MAX_REVIEW_DRAFTS = 5
