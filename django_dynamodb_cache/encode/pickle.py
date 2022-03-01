import pickle

from django_dynamodb_cache.encode.base import BaseEncode


class PickleEncode(BaseEncode):
    PROTOCOL = pickle.HIGHEST_PROTOCOL

    @classmethod
    def dumps(cls, value):
        return pickle.dumps(value, cls.PROTOCOL)

    @classmethod
    def loads(cls, value):
        return pickle.loads(value)
