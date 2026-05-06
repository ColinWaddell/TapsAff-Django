from django.apps import AppConfig


class WWWConfig(AppConfig):
    name = "www"
    # Tables in this app are tiny (a few dozen rows of weather/clothing
    # icons), so the existing 32-bit AutoField PKs are correct. Setting
    # this explicitly silences the Django 3.2+ W042 warning without
    # forcing a migration to BigAutoField.
    default_auto_field = "django.db.models.AutoField"
