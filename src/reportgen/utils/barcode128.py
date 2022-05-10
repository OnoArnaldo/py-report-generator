import csv
from pathlib import Path
from dataclasses import dataclass
from functools import cache
from .base import Base

ROOT = Path(__file__).parent
DATA_DIR = ROOT.joinpath('data')


@dataclass
class Barcode(Base):
    filename: Path
    column: str
    start: str
    stop: str


@dataclass
class Value(Base):
    value: str
    hex: str
    A: str
    B: str
    C: str
    code: str
    latin1: str
    pattern: str
    width: float


barcodes = {
    '128A': Barcode(DATA_DIR.joinpath('barcode128.csv'), 'A', 'Start Code A', 'Stop'),
    '128B': Barcode(DATA_DIR.joinpath('barcode128.csv'), 'B', 'Start Code B', 'Stop'),
    '128C': Barcode(DATA_DIR.joinpath('barcode128.csv'), 'C', 'Start Code C', 'Stop'),
}
final_bar = '2'


@cache
def get_codes(fname: Path | str, column: str = '128C') -> dict:
    res = {}
    with open(fname) as f:
        reader = csv.reader(f)
        for row in reader:
            value = Value(*row)
            res[getattr(value, column)] = value.replace(value=int(value.value))
    f.close()
    return res


def _adjust_size(value: str) -> str:
    size = len(value)
    zero = '0' * (size % 2)
    return zero + value


def barcode(value: str, key: str = '128C') -> list[int]:
    value = _adjust_size(value)

    bc = barcodes.get(key)
    codes = get_codes(bc.filename, bc.column)

    start = codes[bc.start]
    ret = start.width
    check = start.value

    pos = 1
    for i in range(0, len(value), 2):
        v = value[i:i + 2]

        code = codes[v]
        ret += code.width
        check += code.value * pos

        pos += 1

    checksum = codes[f'{check % 103:0>2}']
    ret += checksum.width

    stop = codes[bc.stop]
    ret += stop.width + final_bar

    return ret
