SECRET_KEY = "django-insecure-jv!jxo%un3wse2^#s2_e$awvo1-cpb1z-)f7o14nry-9se7=ui"

INSTALLED_APPS = [
    "django_dynamodb_cache",
]

CACHES = {
    "default": {
        "BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend",
        "LOCATION": "django-dynamodb-cache",
        "TIMEOUT": 60,
        "MAX_ENTRIES": 300,
        "KEY_PREFIX": "django-dynamodb-cache",
        "VERSION": 1,
        "OPTIONS": {},
    },
    "replica": {"BACKEND": "django_dynamodb_cache.backend.DjangoCacheBackend"},
}
USE_TZ = False
