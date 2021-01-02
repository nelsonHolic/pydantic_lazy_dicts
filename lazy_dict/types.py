from typing import Generic, Dict, MutableMapping, TypeVar

KEY = TypeVar('KEY')  # Can be Hashable
VALUE = TypeVar('VALUE')  # Can be anything


class _LazyDict(MutableMapping):

    def __init__(self, model, *args, **kwargs):
        self.model = model
        self.store = dict(*args, **kwargs)

    def __getitem__(self, key: KEY) -> VALUE:
        obj = self.store[key]

        if isinstance(obj, self.model):
            return obj

        obj = self.model.parse_obj(obj)
        self.store[key] = obj
        return obj

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class LazyDict(Generic[KEY, VALUE], Dict[KEY, VALUE]):

    def __init__(self, model):
        super().__init__()
        self.__model__ = model

    def __class_getitem__(cls, item):
        return cls(item[1])

    def __call__(self, *args, **kwargs):
        return _LazyDict(self.__model__, *args, **kwargs)

    def __get_validators__(self):
        yield self.validate

    def validate(self, v):
        return _LazyDict(self.__model__, v)
