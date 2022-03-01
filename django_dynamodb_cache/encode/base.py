class BaseEncode:
    @classmethod
    def dumps(cls, value):
        raise NotImplementedError

    @classmethod
    def loads(cls, value):
        raise NotImplementedError
