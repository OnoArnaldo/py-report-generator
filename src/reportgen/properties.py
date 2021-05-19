from collections import namedtuple
from reportlab.lib.units import cm
from .enums import FontAlign

Font = namedtuple('Font', 'family size align', defaults=['Courier', 10, FontAlign.LEFT])


class Size(namedtuple('Size', 'width height', defaults=[0, 0])):
    def __repr__(self):
        return f'Size({self.width/cm:.2f}, {self.height/cm:.2f})'


class Position(namedtuple('Position', 'top left', defaults=[0, 0])):
    def __repr__(self):
        return f'Position({self.top/cm:.2f}, {self.left/cm:.2f})'


class Margin(namedtuple('Margin', 'top left bottom right', defaults=[0, 0, 0, 0])):
    def __repr__(self):
        return f'Margin({self.top/cm:.2f}, {self.left/cm:.2f}, {self.bottom/cm:.2f}, {self.right/cm:.2f})'

    @property
    def horizontal(self):
        return self.left + self.right

    @property
    def vertical(self):
        return self.top + self.bottom


class Element:
    def __init__(self, name: str, position: Position = None, size: Size = None):
        self.name = name
        self.position = position or Position()
        self.size = size or Size()

    def __repr__(self):
        return f'{self.name}({self.position}, {self.size})'
