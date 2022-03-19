from random import random

SECRET_KEY = "django-insecure-jv!jxo%un3wse2^#s2_e$awvo1-cpb1z-)f7o14nry-9se7=ui"

INSTALLED_APPS = [
    "django_dynamodb_cache",
]

CACHES = {
    "default": {
        "BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend",
        "LOCATION": f"test-django-dynamodb-cache-{random()}",
        "TIMEOUT": 60,
        "MAX_ENTRIES": 300,
        "KEY_PREFIX": "django-dynamodb-cache",
        "VERSION": 1,
        "OPTIONS": {
            "aws_region_name": "us-east-1",
        },
    },
    "replica": {
        "BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend",
        "LOCATION": f"test-django-dynamodb-cache-{random()}",
    },
}
USE_TZ = False
