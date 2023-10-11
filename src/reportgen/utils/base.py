import typing as _
from dataclasses import fields

BaseT = _.TypeVar('BaseT', bound='Base')


class Base:
    def __getitem__(self: BaseT, item: int | str) -> _.Any:
        match item:
            case int(idx):
                f = fields(self)[idx]
                return getattr(self, f.name)
            case str(key):
                return getattr(self, key)

    def keys(self: BaseT) -> list:
        return [f.name for f in fields(self)]

    def replace(self: BaseT, **kwargs) -> BaseT:
        new_kwargs = {**self, **kwargs}
        return self.__class__(**new_kwargs)
