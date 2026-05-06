"""Test settings for tapsaff.

Imports the main settings module and overrides anything that should differ
when running tests:

* CACHES → DummyCache so caching never interferes with test assertions.
* DATABASES → SQLite in-memory so each test run starts with a fresh schema.
* DEBUG → False so tests behave like production.

Run tests with::

    DJANGO_SETTINGS_MODULE=tapsaff.settings_test python manage.py test
"""
from .settings import *  # noqa: F401,F403

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
