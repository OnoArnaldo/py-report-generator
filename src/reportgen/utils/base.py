import typing as _
from dataclasses import fields

TBase = _.TypeVar('TBase', bound='Base')


class Base:
    def __getitem__(self: TBase, item: int | str) -> _.Any:
        match item:
            case int(idx):
                f = fields(self)[idx]
                return getattr(self, f.name)
            case str(key):
                return getattr(self, key)

    def keys(self: TBase) -> list:
        return [f.name for f in fields(self)]

    def replace(self: TBase, **kwargs) -> TBase:
        new_kwargs = {**self, **kwargs}
        return self.__class__(**new_kwargs)
