from django.conf import settings as base_settings

from django_dynamodb_cache.helper import import_string

MEMCACHE_MAX_KEY_LENGTH = 250


class Defaults:
    CACHEOPS_ENABLED = True
    CACHEOPS_REDIS = {}
    CACHEOPS_DEFAULTS = {}
    CACHEOPS = {}
    CACHEOPS_PREFIX = ""
    CACHEOPS_LRU = False
    CACHEOPS_CLIENT_CLASS = None
    CACHEOPS_DEGRADE_ON_FAILURE = False
    CACHEOPS_SENTINEL = {}
    # NOTE: we don't use this fields in invalidator conditions since their values could be very long
    #       and one should not filter by their equality anyway.
    CACHEOPS_SKIP_FIELDS = "FileField", "TextField", "BinaryField", "JSONField"
    CACHEOPS_LONG_DISJUNCTION = 8

    FILE_CACHE_DIR = "/tmp/cacheops_file_cache"
    FILE_CACHE_TIMEOUT = 60 * 60 * 24 * 30


class Settings:
    def __getattr__(self, name):
        res = getattr(base_settings, name, getattr(Defaults, name))
        if name == "CACHEOPS_PREFIX":
            res = res if callable(res) else import_string(res)

        # Convert old list of classes to list of strings
        if name == "CACHEOPS_SKIP_FIELDS":
            [f if isinstance(f, str) else f.get_internal_type(res) for f in res]

        # Save to dict to speed up next access, __getattr__ won't be called
        self.__dict__[name] = res
        return res

    def __init__(self, **kwargs):
        self.encode = "django_dynamodb_cache.encode.PickleEncode"
        self.timeout = 120

        self.table_name = "django_dynamodb_cache"
        self.version = 1
        self.key_prefix = "django_dynamodb_cache"
        self.key_func = lambda p, k, v: f"{p}:{k}:{v}"

        self.key_column = "cache_key"
        self.expiration_column = "cache_expiration"
        self.content_column = "content"

        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.aws_region_name = "us-east-1"

        self.read_capacity_units = 1
        self.write_capacity_units = 1

        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

        if hasattr(self, "key_function"):
            self.key_func = self.module(self.key_function)

    def get(self, key):
        value = getattr(self, key)
        if not value:
            raise AttributeError("Key %s not exists in settings", key)

        return value

    def module(self, key, *args, **kwargs):
        path = self.get(key)
        return import_string(path)

    def instance(self, key, *args, **kwargs):
        path = self.get(key)
        return import_string(path)(*args, **kwargs)

    def __getitem__(self, key):
        return self.get(key)
