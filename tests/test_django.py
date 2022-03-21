import os
import shutil

import django
from django.conf import settings
from django.core.cache import caches
from django.core.management import call_command
from django.test import TestCase

from django_dynamodb_cache.backend import DjangoCacheBackend
from django_dynamodb_cache.dynamodb import get_table

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings.settings"
django.setup()


class TestDjango(TestCase):
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


# class TestDjangoApp(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.settings = Settings(aws_region_name="us-east-1", table_name=TABLE_NAME)
#         cls.dynamodb = get_dynamodb(cls.settings)
#         cls.cache = Cache(cls.settings)
#         cls.table = create_table(cls.settings, cls.dynamodb)
#         super().setUpClass()

#     @classmethod
#     def teardown_class(cls):
#         cls.table.delete(
#             TableName=cls.settings.table_name,
#         )
#         super().tearDownClass()
