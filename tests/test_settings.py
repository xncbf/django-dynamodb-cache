from django_dynamodb_cache import Cache
from django_dynamodb_cache.settings import Settings


def test_simples():
    settings = Settings(version=10)

    assert settings["version"] == settings.version
    assert settings.get("version") == settings.version
    assert settings.version == 10


def test_encode():
    settings = Settings(encode="json")

    cache = Cache(settings)

    j = cache.encode.dumps({"a": 99})
    assert j == '{"a": 99}'
