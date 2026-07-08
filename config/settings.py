"""
Django settings for the OJT Placement Tracking System.

IMPORTANT: Django's built-in admin site (django.contrib.admin urls) is
intentionally NOT wired up in config/urls.py, and no models are registered
with it. All data management is done through custom views/templates in the
`placement` app, per the assignment requirement that prohibits use of the
default Django Admin Panel.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-change-this-key-before-deploying-anywhere"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    # kept for sessions / auth password hashers / static files support only.
    # NOTE: 'django.contrib.admin' is deliberately left out of urls.py.
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "placement",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "placement" / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom session key used to store the logged-in School Admin's admin_id
ADMIN_SESSION_KEY = "school_admin_id"

LOGIN_URL = "/login/"
