from django.core.cache.backends.base import default_key_func

from .helper import import_string

MEMCACHE_MAX_KEY_LENGTH = 250


class Settings(object):
    def __init__(self, **kwargs):
        # defaults
        self.encode = "django_dynamodb_cache.encode.PickleEncode"
        self.timeout = 120

        self.table_name = "django_dynamodb_cache"
        self.version = 1
        self.key_prefix = "django_cache"
        self.key_func = lambda p, k, v: f"{p}:{k}:{v}"

        self.key_column = "cache_key"
        self.expiration_column = "expiration"
        self.content_column = "content"

        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.aws_region_name = None

        self.is_on_demand = True
        self.read_capacity_units = 1
        self.write_capacity_units = 1

        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

        if hasattr(self, "key_function"):
            self.key_func = self.get_key_func(self.key_function)

    def get_key_func(self, key_func):
        """
        Function to decide which key function to use.
        Default to ``default_key_func``.
        """
        if key_func is not None:
            if callable(key_func):
                return key_func
            else:
                return import_string(key_func)
        return default_key_func

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
