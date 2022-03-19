from unittest import TestCase, mock

from django_dynamodb_cache import Cache
from django_dynamodb_cache.dynamodb import create_table, get_dynamodb
from django_dynamodb_cache.settings import Settings

from .conf import TABLE_NAME


class TestCacheSimple(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = Settings(aws_region_name="us-east-1", table_name=TABLE_NAME)
        cls.dynamodb = get_dynamodb(cls.settings)
        cls.cache = Cache(cls.settings)
        cls.table = create_table(cls.settings, cls.dynamodb)
        super().setUpClass()

    @classmethod
    def teardown_class(cls):
        cls.table.delete(
            TableName=cls.settings.table_name,
        )
        super().tearDownClass()

    def test_set_simple(self):
        self.cache.set("test-django-dynamodb-cache", "too much love")
        item = self.cache.get("test-django-dynamodb-cache")
        self.assertEqual(item, "too much love")

        self.cache.delete("test-django-dynamodb-cache")
        value = self.cache.get("test-django-dynamodb-cache", 1001)
        self.assertEqual(value, 1001)

    # def test_get_delete_many(self):

    #     items = {f"test-django-dynamodb-cache_{i}": f"too much love {i}" for i in range(10)}

    #     self.cache.set_many(items)
    #     from_cache = self.cache.get_many(items.keys())
    #     self.assertEqual(items, from_cache)
    #     self.cache.delete_many(items.keys())

    #     value = self.cache.get("test-django-dynamodb-cache_1", 1001)
    #     self.assertEqual(value, 1001)

    def test_add(self):
        self.cache.set("test_add", "some set")
        self.cache.add("test_add", "another add")
        value = self.cache.get("test_add", "default")
        self.assertEqual(value, "some set")

    def test_expired(self):
        self.cache.set("expired", "lost data", -1000)
        value = self.cache.get("expired", 1001)

        self.assertEqual(value, 1001)

    def test_incr_dec_version(self):
        self.cache.set("incr", 1001, version=10)
        self.cache.decr_version("incr", version=10)
        value = self.cache.get("incr", version=9)
        self.assertEqual(value, 1001)

    @mock.patch("warnings.warn")
    def test_verify_key(self, mock_warn):
        BIG = "0" * 251
        self.cache.validate_key(BIG)
        mock_warn.assert_called()

        mock_warn.reset_mock()
        invalid = " "
        self.cache.validate_key(invalid)
        mock_warn.assert_called()

    @mock.patch("warnings.warn")
    def test_clean(self, mock_warn):
        self.cache.clear()
        mock_warn.assert_called()

    def test_incr_decr_value(self):

        self.cache.set("i", 10)
        self.cache.decr("i", 42)
        value = self.cache.get("i")
        self.assertEqual(value, -32)
