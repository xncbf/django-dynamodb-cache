from unittest.mock import patch

from django_dynamodb_cache.cache import Cache


def test_set_simple(cache: Cache):
    cache.set("set_simple", "test")
    item = cache.get("set_simple")
    assert item == "test"

    cache.set("set_simple", "test2")
    item = cache.get("set_simple")
    assert item == "test2"

    cache.delete("set_simple")
    value = cache.get("set_simple", 1001)
    assert value == 1001


def test_get_delete_many(cache: Cache):
    items = {f"get_delete_many_{i}": f"test {i}" for i in range(10)}

    cache.set_many(items)
    from_cache = cache.get_many(items.keys())
    assert items == from_cache
    cache.delete_many(items.keys())

    value = cache.get("get_delete_many_1", 1001)
    assert value == 1001


def test_add(cache: Cache):
    cache.add("test_add", "some set")
    cache.add("test_add", "another add")
    value = cache.get("test_add", "default")
    assert value == "some set"


def test_expired(cache: Cache):
    cache.set("expired", "lost data", -1000)
    value = cache.get("expired", 1001)
    assert value == 1001


def test_incr_dec_version(cache: Cache):
    cache.set("incr", 1001, version=10)
    cache.decr_version("incr", version=10)
    value = cache.get("incr", version=9)
    assert value == 1001


@patch("warnings.warn")
def test_verify_key(mock_warn, cache: Cache):
    BIG = "0" * 251
    cache.validate_key(BIG)
    mock_warn.assert_called()

    mock_warn.reset_mock()
    invalid = " "
    cache.validate_key(invalid)
    mock_warn.assert_called()


def test_clear(cache: Cache):
    cache.set("key_1", "value_1")
    cache.set("key_2", "value_2")
    cache.set("key_3", "value_3")

    assert cache.get("key_1") == "value_1"
    assert cache.get("key_2") == "value_2"
    assert cache.get("key_3") == "value_3"

    cache.clear()

    assert cache.get("key_1") is None
    assert cache.get("key_2") is None
    assert cache.get("key_3") is None


def test_incr_decr_value(cache: Cache):
    cache.set("i", 10)
    cache.decr("i", 42)
    value = cache.get("i")
    assert value == -32


def test_touch(cache: Cache):
    value = cache.touch("touch")
    assert value["ResponseMetadata"]["HTTPStatusCode"] == 200


def test_get_or_set(cache: Cache):
    value = cache.get("get_or_set")
    assert value is None
    value = cache.get_or_set("get_or_set", 10)
    assert value == 10
    value = cache.get_or_set("get_or_set", 11)
    assert value == 10
    cache.delete("get_or_set")
    value = cache.get("get_or_set")
    assert value is None
    value = cache.get_or_set("get_or_set", lambda: 12)
    assert value == 12
