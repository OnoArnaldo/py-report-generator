from abc import ABC
from typing import ClassVar
from functools import cached_property
from PIL import Image as _Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import pica
from reportlab.lib.utils import ImageReader
from .properties import Size, Margin, Element, Position, Font, Dashes
from .enums import FontAlign


class ReportElement:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

        self._size = Size()
        self._margin = Margin()

        self.parent = Element('Parent')
        self.sibling = Element('Sibling')
        self.child = Element('Child')

    def parent_size(self, width: float, height: float) -> 'ReportElement':
        self.parent.size = Size(width, height)
        return self

    def parent_position(self, top: float, left: float) -> 'ReportElement':
        self.parent.position = Position(top, left)
        return self

    def margin(self, *values) -> 'ReportElement':
        if len(values) == 1:
            m = values * 4
        elif len(values) == 2:
            m = values * 2
        else:
            m = values

        self._margin = Margin(*m)
        return self

    @cached_property
    def calculated_top(self) -> float:
        return self.parent.position.top + self._margin.top

    @cached_property
    def calculated_left(self) -> float:
        return self.parent.position.left + self._margin.left

    @cached_property
    def calculated_width(self) -> float:
        adjusted_width = self.parent.size.width - self._margin.horizontal

        if self._size.width:
            return min(self._size.width, adjusted_width)
        return adjusted_width

    @cached_property
    def calculated_height(self) -> float:
        adjusted_height = self.parent.size.height - self._margin.vertical

        if self._size.height:
            return min(self._size.height, adjusted_height)
        return adjusted_height

    def build_sibling(self, element: ClassVar['ReportElement']) -> 'ReportElement':
        return element(self.canvas) \
            .parent_size(*self.sibling.size) \
            .parent_position(*self.sibling.position)

    def build_child(self, element: ClassVar['ReportElement']) -> 'ReportElement':
        return element(self.canvas) \
            .parent_size(*self.child.size) \
            .parent_position(*self.child.position)

    def _update_sibling(self):
        self.sibling.position = Position(
            self.parent.position.top + self.calculated_height + self._margin.vertical,
            self.parent.position.left
        )

        self.sibling.size = self.parent.size._replace(
            height=self.parent.size.height - self.calculated_height - self._margin.vertical
        )

    def _update_child(self):
        self.child.position = Position(
            self.parent.position.top + self._margin.top,
            self.parent.position.left + self._margin.left
        )

        start = Position(self.calculated_top, self.calculated_left)
        end = Position(self.calculated_top + self.calculated_height, self.calculated_left + self.calculated_width)
        self.child.size = Size(
            end.left - start.left,
            end.top - start.top
        )

    def draw(self) -> 'ReportElement':
        raise NotImplementedError('Method "draw" was not implemented.')


class Box(ReportElement, ABC):
    def __init__(self, canvas: Canvas):
        super(Box, self).__init__(canvas)

        self._radius = 5.0
        self._stroke = 1

    def size(self, width: float, height: float) -> 'ReportElement':
        self._size = Size(width, height)
        return self

    def radius(self, radius: float) -> 'ReportElement':
        self._radius = radius
        return self

    def stroke(self, stroke: float) -> 'ReportElement':
        self._stroke = stroke
        return self


class Row(Box):
    def height(self, height: float = 0.0) -> 'ReportElement':
        return self.size(0.0, height)

    def draw(self) -> 'Row':
        if self._stroke != 0:
            self.canvas.roundRect(
                self.calculated_left, self.calculated_top,
                self.calculated_width, self.calculated_height,
                self._radius, self._stroke
            )

        self._update_sibling()
        self._update_child()

        return self


class Column(Box):
    def width(self, width: float = 0.0) -> 'ReportElement':
        return self.size(width, 0.0)

    def _update_sibling(self):
        self.sibling.position = Position(
            self.parent.position.top,
            self.parent.position.left + self.calculated_width + self._margin.horizontal
        )

        self.sibling.size = self.parent.size._replace(
            width=self.parent.size.width - self.calculated_width - self._margin.horizontal
        )

    def draw(self) -> 'Column':
        if self._stroke != 0:
            self.canvas.roundRect(
                self.calculated_left, self.calculated_top,
                self.calculated_width, self.calculated_height,
                self._radius, self._stroke
            )

        self._update_sibling()
        self._update_child()

        return self


class Text(ReportElement):
    def __init__(self, canvas: Canvas):
        super(Text, self).__init__(canvas)

        self._value = ''
        self._font = Font()

    def value(self, value: str) -> 'Text':
        self._value = value
        return self

    def font(self, family: str, size: int, align: FontAlign = FontAlign.LEFT) -> 'Text':
        self._font = Font(family, size, align)
        return self

    @cached_property
    def calculated_font_size(self) -> float:
        return (self._font.size/12) * pica

    @cached_property
    def calculated_height(self) -> float:
        return self.calculated_font_size

    @cached_property
    def calculated_top(self) -> float:
        return self.parent.position.top + self._margin.top + self.calculated_font_size

    @cached_property
    def calculated_left(self) -> float:
        if self._font.align == FontAlign.LEFT:
            return self.parent.position.left + self._margin.left
        elif self._font.align == FontAlign.CENTER:
            return self.parent.position.left + (self.parent.size.width / 2)
        elif self._font.align == FontAlign.RIGHT:
            return self.parent.position.left + self.parent.size.width - self._margin.right
        return 0

    def draw(self) -> 'Text':
        self.canvas.saveState()
        self.canvas.setFont(self._font.family, self._font.size)

        if self._font.align == FontAlign.LEFT:
            self.canvas.drawString(
                self.calculated_left, self.calculated_top,
                self._value
            )
        elif self._font.align == FontAlign.CENTER:
            self.canvas.drawCentredString(
                self.calculated_left, self.calculated_top,
                self._value
            )
        elif self._font.align == FontAlign.RIGHT:
            self.canvas.drawRightString(
                self.calculated_left, self.calculated_top,
                self._value
            )

        self.canvas.restoreState()

        self._update_sibling()

        return self

    def build_child(self, element: 'ReportElement') -> 'ReportElement':
        raise Exception('Not allowed to call this method in "Text".')


class Image(ReportElement):
    def __init__(self, canvas: Canvas):
        super(Image, self).__init__(canvas)

        self._filename = ''

    def filename(self, _filename: str) -> 'Image':
        self._filename = _filename
        return self

    def _image_reader(self) -> ImageReader:
        with _Image.open(self._filename) as image:
            image = image.transpose(_Image.FLIP_TOP_BOTTOM)

        return ImageReader(image)

    def draw(self) -> 'Image':
        self.canvas.drawImage(
            self._image_reader(),
            self.calculated_left, self.calculated_top,
            self.calculated_width, self.calculated_height,
            preserveAspectRatio=True
        )

        self._update_sibling()

        return self

    def build_child(self, element: 'ReportElement') -> 'ReportElement':
        raise Exception('Not allowed to call this method in "Image".')


class Line(ReportElement):
    def __init__(self, canvas: Canvas):
        super(Line, self).__init__(canvas)

        self._dashes = Dashes()
        self._stroke = 1

    def dashes(self, *pattern) -> 'Line':
        self._dashes = Dashes(pattern)
        return self

    def stroke(self, stroke: float) -> 'Line':
        self._stroke = stroke
        return self

    @cached_property
    def calculated_height(self) -> float:
        return self._stroke

    def draw(self) -> 'Line':
        self.canvas.saveState()
        self.canvas.setDash(self._dashes.pattern)
        self.canvas.setLineWidth(self._stroke)
        self.canvas.line(
            self.calculated_left, self.calculated_top,
            self.calculated_width, self.calculated_top
        )
        self.canvas.restoreState()

        self._update_sibling()
        return self

    def build_child(self, element: 'ReportElement') -> 'ReportElement':
        raise Exception('Not allowed to call this method in "Image".')


class PageBreak:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw(self) -> 'PageBreak':
        self.canvas.showPage()
        return self
