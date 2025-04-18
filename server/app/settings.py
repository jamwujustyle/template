from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-l*fp_87mc4om#)1lsqp3(h-p2inoi_p48zbknfrd4fx_xeb_x0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")


# Application definition

INSTALLED_APPS = [
    # CONFIGS
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    # APPS
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "no-name"),
        "USER": os.environ.get("DB_USER", "no-user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "no-pass"),
        "HOST": os.environ.get("DB_HOST", "no-host"),
        "PORT": os.environ.get("DB_PORT", "no-port"),
    }
}
print(os.environ.get("DB_NAME"))
print(os.environ.get("DB_USER"))
print(os.environ.get("DB_PASSWORD"))
print(os.environ.get("DB_HOST"))
print(os.environ.get("DB_PORT"))
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated"),
}

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
#     },
#     {
#         "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
#     },
# ]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
