import time
import warnings
from decimal import Decimal

from django.core.cache.backends.base import BaseCache

from .dynamodb import get_dynamodb, get_table
from .exceptions import CacheKeyWarning
from .helper import logger
from .settings import MEMCACHE_MAX_KEY_LENGTH


class Cache(BaseCache):
    def __init__(self, settings):

        self.version = settings.version
        self.key_func = settings.key_func
        self.key_prefix = settings.key_prefix
        self.timeout = settings.timeout

        self.dynamodb = get_dynamodb(settings)
        self.table = get_table(settings, self.dynamodb)

        self.encode = settings.module("encode")

        self.settings = settings

    def make_expiration(self, timeout):
        timeout = timeout or self.timeout
        timeout_d = Decimal(timeout)
        now = Decimal(time.time())
        return now + timeout_d

    def make_key(self, key, version=None):
        """
        Construct the key used by all other methods. By default, use the
        key_func to generate a key (which, by default, prepends the
        `key_prefix' and 'version'). A different key function can be provided
        at the time of cache construction; alternatively, you can subclass the
        cache backend to provide custom key making behavior.
        """
        if version is None:
            version = self.version

        new_key = self.key_func(self.key_prefix, key, version)
        return new_key

    def make_item(self, key, expiration, value):
        return {
            self.settings.key_column: key,
            self.settings.expiration_column: expiration,
            self.settings.content_column: value,
        }

    def add(self, key, value, timeout=None, version=None):
        if self.has_key(key, version):  # noqa: W601
            return False
        self.set(key, value, timeout, version)
        logger.debug('Add "%s" on dynamodb "%s" table', key, self.table.table_name)
        return True

    def get(self, key, default=None, version=None):
        key = self.make_key(key, version)

        response = self.table.get_item(Key={self.settings.key_column: key})

        if "Item" not in response:
            logger.debug(
                'Get EMPTY value for "%s" on dynamodb "%s" table',
                key,
                self.table.table_name,
            )
            return default

        item = response["Item"]
        if item[self.settings.expiration_column] < self.make_expiration(1):
            logger.debug(
                'Get EXPIRED value for "%s" on dynamodb "%s" table',
                key,
                self.table.table_name,
            )
            return default

        value = item[self.settings.content_column]
        logger.debug('Get for "%s" on dynamodb "%s" table', key, self.table.table_name)
        value = self.encode.loads(value.value)
        return value

    def set(self, key, value, timeout=None, version=None, batch=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        expiration = self.make_expiration(timeout)
        value = self.encode.dumps(value)

        table = batch or self.table

        if not self.has_key(key, version):  # noqa: W601
            response = table.put_item(Item=self.make_item(key, expiration, value))
        else:
            response = table.update_item(  # noqa
                Key={self.settings.key_column: key},
                UpdateExpression=f"SET {self.settings.expiration_column} = :ex,  {self.settings.content_column} = :vl",
                ExpressionAttributeValues={":ex": expiration, ":vl": value},
            )

        logger.debug(
            'Set "%s" with "%s" timout on dynamodb "%s" table',
            key,
            timeout,
            self.table.table_name,
        )

    def touch(self, key, timeout=None, version=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)
        expiration = self.make_expiration(timeout)
        item = self.table.update_item(
            Key={self.settings.key_column: key},
            UpdateExpression=f"SET {self.settings.expiration_column} = :ex",
            ExpressionAttributeValues={":ex": expiration},
        )
        logger.debug(
            'Reset expiration "%s" to %s on dynamodb "%s" table',
            key,
            timeout,
            self.table.table_name,
        )
        return item

    def delete(self, key, version=None, batch=None):
        key = self.make_key(key, version=version)
        self.validate_key(key)

        table = batch or self.table

        table.delete_item(Key={self.settings.key_column: key})
        logger.debug("Delete %s on dynamodb %s table", key, self.settings.table_name)

    def delete_many(self, keys, version=None):
        """
        Delete a bunch of values in the cache at once.
        """

        with self.table.batch_writer() as batch:
            for key in keys:
                self.delete(key, version=version, batch=batch)

    def set_many(self, data, timeout=None, version=None):
        """
        Set a bunch of values in the cache at once from a dict of key/value
        pairs.

        If timeout is given, use that timeout for the key; otherwise use the
        default cache timeout.

        On backends that support it, return a list of keys that failed
        insertion, or an empty list if all keys were inserted successfully.
        """

        with self.table.batch_writer() as batch:
            for key, value in data.items():
                self.set(key, value, timeout=timeout, version=version, batch=batch)
        return []

    def has_key(self, key, version=None):
        key = self.make_key(key, version)

        response = self.table.get_item(
            Key={self.settings.key_column: key},
            ReturnConsumedCapacity="NONE",
            # ProjectionExpression=self.settings.key_column,
        )
        return "Item" in response

    def clear(self):
        warnings.warn("Clean is not supported yet.")

    def get_many(self, keys, version=None):
        """
        Fetch a bunch of keys from the cache. For certain backends (memcached,
        pgsql) this can be *much* faster when fetching multiple values.

        Return a dict mapping each key in keys to its value. If the given
        key is missing, it will be missing from the response dict.
        """
        d = {}
        for k in keys:
            val = self.get(k, version=version)
            if val is not None:
                d[k] = val
        return d

    # region copy from django

    def get_or_set(self, key, default, timeout=None, version=None):
        """
        Fetch a given key from the cache. If the key does not exist,
        add the key and set it to the default value. The default value can
        also be any callable. If timeout is given, use that timeout for the
        key; otherwise use the default cache timeout.

        Return the value of the key stored or retrieved.
        """
        val = self.get(key, version=version)
        if val is None:
            if callable(default):
                default = default()
            if default is not None:
                self.add(key, default, timeout=timeout, version=version)
                # Fetch the value again to avoid a race condition if another
                # caller added a value between the first get() and the add()
                # above.
                return self.get(key, default, version=version)
        return val

    def incr(self, key, delta=1, version=None):
        """
        Add delta to value in the cache. If the key does not exist, raise a
        ValueError exception.
        """
        value = self.get(key, version=version)
        if value is None:
            raise ValueError("Key '%s' not found" % key)
        new_value = value + delta
        self.set(key, new_value, version=version)
        return new_value

    def decr(self, key, delta=1, version=None):
        """
        Subtract delta from value in the cache. If the key does not exist, raise
        a ValueError exception.
        """
        return self.incr(key, -delta, version=version)

    def __contains__(self, key):
        """
        Return True if the key is in the cache and has not expired.
        """
        # This is a separate method, rather than just a copy of has_key(),
        # so that it always has the same functionality as has_key(), even
        # if a subclass overrides it.
        return self.has_key(key)  # noqa: W601

    def validate_key(self, key):
        """
        Warn about keys that would not be portable to the memcached
        backend. This encourages (but does not force) writing backend-portable
        cache code.
        """
        if len(key) > MEMCACHE_MAX_KEY_LENGTH:
            warnings.warn(
                "Cache key will cause errors if used with memcached: %r "
                "(longer than %s)" % (key, MEMCACHE_MAX_KEY_LENGTH),
                CacheKeyWarning,
            )
        for char in key:
            if ord(char) < 33 or ord(char) == 127:
                warnings.warn(
                    "Cache key contains characters that will cause errors if " "used with memcached: %r" % key,
                    CacheKeyWarning,
                )
                break

    def incr_version(self, key, delta=1, version=None):
        """
        Add delta to the cache version for the supplied key. Return the new version.
        """
        if version is None:
            version = self.version

        value = self.get(key, version=version)
        if value is None:
            raise ValueError("Key '%s' not found" % key)

        self.set(key, value, version=version + delta)
        self.delete(key, version=version)
        return version + delta

    def decr_version(self, key, delta=1, version=None):
        """
        Subtract delta from the cache version for the supplied key. Return the new version.
        """
        return self.incr_version(key, -delta, version)

    def close(self, **kwargs):
        """Close the cache connection"""
        logger.info("Close connection with %s table", self.table.table_name)
