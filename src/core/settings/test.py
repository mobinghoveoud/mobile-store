from .base import *  # noqa: F403

DEBUG = False

LANGUAGE_CODE = "en"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",  # noqa: F405
    }
}
