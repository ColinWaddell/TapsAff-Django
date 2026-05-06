"""
Django settings for tapsaff project.
"""
import environ
import os

root = environ.Path(__file__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env(DEBUG=(bool, False))
# read_env() defaults to looking next to the calling file (tapsaff/.env),
# but the project's .env lives at the repo root. Pin it explicitly.
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env("DEBUG")


# Quick-start development settings - unsuitable for production
SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "taps-aff.co.uk",
    "api.taps-aff.co.uk",
    "www.taps-aff.co.uk",
]

LOGIN_URL = "/admin/login"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "www.apps.WWWConfig",
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

ROOT_URLCONF = "tapsaff.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "www", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

WSGI_APPLICATION = "tapsaff.wsgi.application"


# Database
DATABASES = {"default": env.db()}


# Cache
# Backend is configured by the CACHE env var as a django-environ cache URL.
# Supported schemes (django-environ 0.4.5):
#   locmemcache://  - in-process LocMemCache (dev default)
#   dummycache://   - DummyCache (no-op, useful for tests)
#   memcache://host:11211
#   rediscache://host:6379/0  (requires django-redis on Django < 4)
#   filecache:///abs/path
#   dbcache://table_name
#
# CACHE_MAP_TIMEOUT controls how long the rendered SVG map is cached.
# Forecast cache TTL is taken from the Settings.cache_seconds model field
# at call time, so it can be tuned without redeploys.

# env.cache_url() trips on an empty CACHE env var (KeyError: '') because
# urlparse('') returns an empty scheme. Strip-and-fall-back makes the
# default kick in regardless of how the env var got cleared.
_cache_url = env.str("CACHE", default="locmemcache://").strip() or "locmemcache://"
CACHES = {"default": env.cache_url_config(_cache_url)}

CACHE_MAP_TIMEOUT = env.int("CACHE_MAP_TIMEOUT", default=3600)


# Django 3.2+ asks projects to declare their default PK type. The existing
# migrations were generated with AutoField (32-bit) and the tables in this
# app are tiny (a few dozen rows of weather/clothing icons), so AutoField
# remains correct - using BigAutoField would require a migration touching
# every model PK with no real-world benefit.

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Session
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_L10N = False

DATETIME_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
]

public_root = root.path("/")

STATIC_URL = "/static/"


# Static files (CSS, JavaScript, Images)
if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
else:
    STATIC_ROOT = public_root("static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "www/static"),
]


# Weather.com Settings
WEATHER_API_ID = env("WEATHER_API_ID")
