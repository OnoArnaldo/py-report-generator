import typing as _
import sys


class MISSINGTYPE:
    def __repr__(self):
        return '<MISSING>'


MISSING = MISSINGTYPE()


def _init_fields(cls: _.Type) -> _.NoReturn:
    fields = {}
    for c in cls.__mro__[-1:0:-1]:
        if (flds := getattr(c, '_fields', None)) is not None:
            for k, v in flds.items():
                fields[k] = v

    for k, v in vars(cls).items():
        if isinstance(v, field):
            v.name = k
            fields[k] = v

    setattr(cls, '_fields', fields)


def _exec(cls: _.Type, code: str) -> _.NoReturn:
    globs = sys.modules[cls.__module__].__dict__
    fs = {}
    exec(code, globs, fs)

    for k, v in fs.items():
        setattr(cls, k, v)


def _build_init(cls: _.Type, frozen: bool = False) -> _.NoReturn:
    code = 'def __init__(self, {args}):\n{setters}'
    args = ', '.join([f'{v.name}={v.defaulter}' for v in cls._fields.values() if v.init])

    if frozen:
        setters = '\n'.join(
            [f'    object.__setattr__(self, {v.name!r}, {v.name})' for v in cls._fields.values() if v.init]
        )
    else:
        setters = '\n'.join([f'    self.{v.name} = {v.setter}' for v in cls._fields.values() if v.init])

    no_init = '\n'.join([f'    self.{v.name} = {v.initiator}' for v in cls._fields.values() if not v.init])
    no_init = f'\n{no_init}' if no_init != '' else ''

    setters = setters + no_init if setters != '' or no_init != '' else '    pass'

    _exec(cls, code.format(args=args, setters=setters))


def _build_repr(cls: _.Type) -> _.NoReturn:
    code = 'def __repr__(self):\n    return f"{clsname}({reprs})"'
    clsname = cls.__name__
    reprs = ', '.join([f'{v.name}: {{self.{v.name}!r}}' for v in cls._fields.values() if v.repr])

    _exec(cls, code.format(clsname=clsname, reprs=reprs))


def _build_readonly(cls: _.Type, frozen: bool = False) -> _.NoReturn:
    if not frozen:
        return

    code = 'def __setattr__(self, key, value):\n' '    raise AttributeError(f"Cannot assign to field \'{key}\'")'
    _exec(cls, code)

    code = 'def __delattr__(self, key):\n' '    raise AttributeError(f"Cannot delete the field \'{key}\'")'
    _exec(cls, code)


def model(cls: _.Type = None, /, *, frozen: bool = False) -> _.Callable:
    """
    Class decorator to build __init__ and __repr__ methods based on the fields.
    """

    def _model(cls: _.Type):
        _init_fields(cls)
        _build_init(cls, frozen)
        _build_repr(cls)
        _build_readonly(cls, frozen)
        return cls

    if cls is None:
        return _model
    return _model(cls)


class field:
    """
    Descriptor to define the field behaviour.
    This is heavily based on dataclasses module, and oversimplified to fit my usage.
    """

    __slots__ = (
        'init',
        'repr',
        'default',
        'default_factory',
        'set_factory',
        'name',
        'field_name',
        'private',
        'field_type',
    )

    def __init__(
        self,
        default: _.Any = MISSING,
        default_factory: _.Callable = MISSING,
        set_factory: _.Callable = MISSING,
        init: bool = True,
        repr: bool = True,
    ):
        self.name = ''
        self.init = init
        self.repr = repr
        self.default = default
        self.default_factory = default_factory
        self.set_factory = set_factory

        self.field_name = ''
        self.private = ''

    def __set_name__(self, owner, name):
        self.field_name = name
        self.private = f'_{name}'

    def __set__(self, instance, value):
        if self.set_factory != MISSING:
            object.__setattr__(instance, self.private, self.set_factory(value))
        else:
            object.__setattr__(instance, self.private, value)

    def __get__(self, instance, owner):
        return getattr(instance, self.private)

    @property
    def setter(self):
        if self.default_factory != MISSING:
            return f'{self.name}()'
        return self.name

    @property
    def defaulter(self):
        if self.default != MISSING:
            return f'{self.default!r}'
        if self.default_factory != MISSING:
            return self.default_factory.__name__
        return 'None'

    @property
    def initiator(self):
        if self.default != MISSING:
            return f'{self.default!r}'
        if self.default_factory != MISSING:
            return f'{self.default_factory.__name__}()'
        return 'None'
