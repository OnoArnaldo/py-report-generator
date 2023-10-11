import typing as _
from xml.etree import ElementTree as _ET
from xmljson import BadgerFish as _BadgerFish, Abdera as _Abdera

if _.TYPE_CHECKING:
    from pathlib import Path

engines = {
    'badgerfish': _BadgerFish,
    'abdera': _Abdera,
}


class InvalidEngine(Exception):
    def __init__(self, engine):
        super().__init__(f'Invalid engine {engine}')


def from_string(text: str, engine: str = 'abdera') -> _.OrderedDict:
    if (eng := engines.get(engine)) is not None:
        return eng(xml_fromstring=False).data(_ET.fromstring(text))
    raise InvalidEngine(engine)


def from_file(fname: 'Path', engine: str = 'abdera') -> _.OrderedDict:
    if (eng := engines.get(engine)) is not None:
        return eng(xml_fromstring=False).data(_ET.parse(fname).getroot())
    raise InvalidEngine(engine)
