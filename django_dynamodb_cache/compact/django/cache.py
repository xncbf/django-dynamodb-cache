from django_dynamodb_cache import Cache, Settings


class DjangoCacheDynamodb(Cache):
    def __init__(self, params):

        table_name = params.get("LOCATION", None)
        timeout = params.get("TIMEOUT", None)
        key_prefix = params.get("KEY_PREFIX", None)
        version = params.get("VERSION", None)
        key_function = params.get(["KEY_FUNCTION"], None)

        options = params.get("OPTIONS", {})
        settings = Settings(  # noqa
            table_name=table_name,
            timeout=timeout,
            key_prefix=key_prefix,
            version=version,
            key_function=key_function ** options,
        )

        super().__init__(params)
