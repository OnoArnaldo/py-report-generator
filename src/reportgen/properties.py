from dataclasses import dataclass, field
from reportlab.lib.units import cm
from .enums import FontAlign
from .utils.base import Base


@dataclass
class Font(Base):
    family: str = 'Courier'
    size: float = 10
    align: FontAlign = FontAlign.LEFT


@dataclass
class Dashes(Base):
    pattern: tuple = field(default_factory=tuple)


@dataclass
class Size(Base):
    width: float = 0
    height: float = 0

    def __repr__(self) -> str:
        return f'Size({self.width/cm:.2f}, {self.height/cm:.2f})'


@dataclass
class Position(Base):
    top: float = 0
    left: float = 0

    def __repr__(self) -> str:
        return f'Position({self.top/cm:.2f}, {self.left/cm:.2f})'


@dataclass
class Margin(Base):
    top: float = 0
    left: float = 0
    bottom: float = 0
    right: float = 0

    def __repr__(self) -> str:
        return f'Margin({self.top/cm:.2f}, {self.left/cm:.2f}, {self.bottom/cm:.2f}, {self.right/cm:.2f})'

    @property
    def horizontal(self) -> float:
        return self.left + self.right

    @property
    def vertical(self) -> float:
        return self.top + self.bottom


@dataclass
class Element(Base):
    name: str
    position: Position = field(default_factory=Position)
    size: Size = field(default_factory=Size)

    def __repr__(self) -> str:
        return f'{self.name}({self.position}, {self.size})'
