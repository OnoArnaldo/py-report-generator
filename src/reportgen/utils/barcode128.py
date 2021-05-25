import os
from typing import Dict, List
from functools import cache
from collections import namedtuple
import csv

ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT, 'data')

Barcode = namedtuple('Barcode', 'filename column start stop')
Value = namedtuple('Value', 'value hex A B C code latin1 pattern width')
barcodes = {
    '128A': Barcode(os.path.join(DATA_DIR, 'barcode128.csv'), 'A', 'Start Code A', 'Stop'),
    '128B': Barcode(os.path.join(DATA_DIR, 'barcode128.csv'), 'B', 'Start Code B', 'Stop'),
    '128C': Barcode(os.path.join(DATA_DIR, 'barcode128.csv'), 'C', 'Start Code C', 'Stop'),
}
final_bar = '2'


@cache
def get_codes(fname: str, column: str = '128C') -> Dict:
    res = {}
    with open(fname) as f:
        reader = csv.reader(f)
        for row in reader:
            value = Value(*row)
            res[getattr(value, column)] = value._replace(value=int(value.value))
    f.close()
    return res


def _adjust_size(value: str) -> str:
    size = len(value)
    zero = '0' * (size % 2)
    return zero + value


def barcode(value: str, key: str = '128C') -> List[int]:
    value = _adjust_size(value)

    bc = barcodes.get(key)
    codes = get_codes(bc.filename, bc.column)

    start = codes[bc.start]
    ret = start.width
    check = start.value

    pos = 1
    for i in range(0, len(value), 2):
        v = value[i:i+2]

        code = codes[v]
        ret += code.width
        check += code.value * pos

        pos += 1

    checksum = codes[f'{check%103:0>2}']
    ret += checksum.width

    stop = codes[bc.stop]
    ret += stop.width + final_bar

    return ret
