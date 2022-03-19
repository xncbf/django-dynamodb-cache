import os
import shutil
from unittest import TestCase

import django
from django.conf import settings
from django.core.cache import caches
from django.core.management import call_command

from django_dynamodb_cache.backend import DjangoCacheBackend
from django_dynamodb_cache.dynamodb import get_table

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings.settings"

# Set up Django
django.setup()


class TestDjangoApp(TestCase):
    @classmethod
    def teardown_class(cls):
        for cache_alias in settings.CACHES:
            cache = caches[cache_alias]
            if isinstance(cache, DjangoCacheBackend):
                backend = DjangoCacheBackend(cache._table, settings.CACHES[cache_alias])
                get_table(backend.settings, backend.dynamodb).delete()

    def test_command(self):
        shutil.rmtree("tests/migrations", True)
        call_command("createcachetable")

    # def test_django_cache(self):
    #     pass
