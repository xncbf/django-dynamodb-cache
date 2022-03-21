from random import random


def make_key(key, key_prefix, version=None):
    return f"{key_prefix}:{version}:{key}"


SECRET_KEY = "django-insecure-jv!jxo%un3wse2^#s2_e$awvo1-cpb1z-)f7o14nry-9se7=ui"

INSTALLED_APPS = [
    "django_dynamodb_cache",
]

CACHES = {
    "default": {
        "BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend",
        "LOCATION": f"test-django-dynamodb-cache-default-{random()}",
        "TIMEOUT": 60,
        "MAX_ENTRIES": 300,
        "KEY_PREFIX": "django-dynamodb-cache",
        "KEY_FUNCTION": "tests.settings.settings.make_key",
        "VERSION": 1,
        "OPTIONS": {
            "aws_region_name": "us-east-1",
            "read_capacity_units": 1,
            "write_capacity_units": 1,
            "encode": "django_dynamodb_cache.encode.PickleEncode",
        },
    },
    "replica": {
        "BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend",
        "LOCATION": f"test-django-dynamodb-cache-{random()}",
    },
}
USE_TZ = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
