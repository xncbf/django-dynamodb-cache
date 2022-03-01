from unittest import TestCase

from django_dynamodb_cache import Cache
from django_dynamodb_cache.settings import Settings


class TestSettings(TestCase):
    def test_simples(self):
        settings = Settings(version=10)

        self.assertEqual(settings["version"], settings.version)
        self.assertEqual(settings.get("version"), settings.version)
        self.assertEqual(settings.version, 10)

    def test_encode(self):
        settings = Settings(encode="json")

        cache = Cache(settings)

        j = cache.encode.dumps({"a": 99})
        self.assertEqual(j, '{"a": 99}')
