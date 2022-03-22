from .cache import Cache
from .settings import Settings


class DjangoCacheBackend(Cache):
    def __init__(self, location, params):
        table_name = location
        timeout = params.get("TIMEOUT", None)
        key_prefix = params.get("KEY_PREFIX", None)
        version = params.get("VERSION", None)
        key_function = params.get("KEY_FUNCTION", None)
        options = params.get("OPTIONS", {})
        settings = Settings(
            table_name=table_name,
            timeout=timeout,
            key_prefix=key_prefix,
            version=version,
            key_function=key_function,
            **options,
        )
        self._table = settings.table_name
        super().__init__(settings)
