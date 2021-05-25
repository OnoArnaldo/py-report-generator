from typing import ClassVar, Tuple, Callable, List
from functools import cached_property
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import pagesizes, units
from .utils.model import model, field
from . import elements as e


@model
class Base:
    name = field(default='')
    font = field(default='')

    parent = field(default=None, repr=False, init=False)
    children = field(default_factory=list, repr=False, init=False)

    @cached_property
    def calculated_page_size(self) -> Tuple:
        if hasattr(self, 'page_size'):
            return getattr(pagesizes, self.page_size.upper())
        if self.parent:
            return self.parent.calculated_page_size
        return pagesizes.A4

    @cached_property
    def calculated_unit(self) -> float:
        if hasattr(self, 'unit'):
            return getattr(units, self.unit.lower())
        if self.parent:
            return self.parent.calculated_unit
        return units.cm

    @cached_property
    def calculated_font(self) -> Tuple:
        if self.font != '':
            family, size, align = self.font.split()
            return family, int(size), getattr(e.FontAlign, align.upper(), e.FontAlign.LEFT)
        elif self.parent:
            return self.parent.calculated_font

    def new_child(self, cls: ClassVar['Base'], *args, **kwargs) -> 'Base':
        child = cls(*args, **kwargs)

        child.parent = self
        self.children.append(child)

        return child


@model
class BaseWithMargin(Base):
    margin = field(default='')

    @cached_property
    def calculated_margin(self) -> List:
        unit = self.calculated_unit
        if isinstance(self.margin, (int, float)):
            margin = [self.margin*unit]
        else:
            margin = list(map(lambda x: float(x)*unit, self.margin.split()))
        if len(margin) == 0:
            return [0.0, 0.0, 0.0, 0.0]
        elif len(margin) == 1:
            return margin * 4
        elif len(margin) == 2:
            return margin * 2
        elif len(margin) == 3:
            return margin + [0.0]
        return margin


class Box:
    def new_row(self, *args, **kwargs) -> 'Row':
        return self.new_child(Row, *args, **kwargs)

    def new_column(self, *args, **kwargs) -> 'Column':
        return self.new_child(Column, *args, **kwargs)

    def new_text(self, *args, **kwargs) -> 'Text':
        return self.new_child(Text, *args, **kwargs)

    def new_image(self, *args, **kwargs) -> 'Image':
        return self.new_child(Image, *args, **kwargs)

    def new_line(self, *args, **kwargs) -> 'Line':
        return self.new_child(Line, *args, **kwargs)

    def new_barcode(self, *args, **kwargs) -> 'Barcode':
        return self.new_child(Barcode, *args, **kwargs)


@model
class Report(Base):
    page_size = field(default='')
    unit = field(default='')

    def new_page(self, *args, **kwargs) -> 'Page':
        return self.new_child(Page, *args, **kwargs)

    def process(self, canvas: Canvas):
        for page in self.children:
            page.process(canvas)


@model
class Page(BaseWithMargin, Box):
    def process(self, canvas: Canvas):
        page = e.Row(canvas)\
            .parent_size(*self.calculated_page_size)\
            .parent_position(0, 0)\
            .margin(*self.calculated_margin)\
            .stroke(0)\
            .draw()

        for idx, child in enumerate(self.children):
            sibling = child.process(page.build_child if idx == 0 else sibling.build_sibling)

        e.PageBreak(canvas).draw()


@model
class Row(BaseWithMargin, Box):
    height = field(default='')
    border = field(default='')

    @cached_property
    def calculated_height(self) -> float:
        return float(self.height or 0) * self.calculated_unit

    @cached_property
    def calculated_border(self) -> float:
        return int(self.border or 0)

    def process(self, builder: Callable):
        row: e.Row = builder(e.Row)\
            .margin(*self.calculated_margin)\
            .height(self.calculated_height)\
            .stroke(self.calculated_border)\
            .draw()

        for idx, child in enumerate(self.children):
            sibling = child.process(row.build_child if idx == 0 else sibling.build_sibling)

        return row


@model
class Column(BaseWithMargin, Box):
    width = field(default='')
    border = field(default='')

    @cached_property
    def calculated_width(self) -> float:
        return float(self.width or 0) * self.calculated_unit

    @cached_property
    def calculated_border(self) -> float:
        return int(self.border or 0)

    def process(self, builder: Callable):
        column = builder(e.Column)\
            .margin(*self.calculated_margin)\
            .width(self.calculated_width)\
            .stroke(self.calculated_border)\
            .draw()

        for idx, child in enumerate(self.children):
            sibling = child.process(column.build_child if idx == 0 else sibling.build_sibling)

        return column


@model
class Text(BaseWithMargin):
    value = field(default='')

    def process(self, builder: Callable):
        return builder(e.Text)\
            .margin(*self.calculated_margin)\
            .font(*self.calculated_font)\
            .value(self.value)\
            .draw()


@model
class Image(BaseWithMargin):
    value = field(default='')

    def process(self, builder: Callable):
        return builder(e.Image)\
            .filename(self.value)\
            .draw()


@model
class Line(BaseWithMargin):
    stroke = field(default='')
    dashes = field(default='')

    @cached_property
    def calculated_stroke(self):
        return int(self.stroke or '0')

    @cached_property
    def calculated_dashes(self):
        return [int(v) for v in self.dashes.split()]

    def process(self, builder: Callable):
        return builder(e.Line)\
            .margin(*self.calculated_margin)\
            .stroke(self.calculated_stroke)\
            .dashes(*self.calculated_dashes)\
            .draw()


@model
class Barcode(BaseWithMargin):
    name = field(default='')
    height = field(default='')
    code_set = field(default='')
    bar_width = field(default='')
    align = field(default='')
    value = field(default='')

    @cached_property
    def calculated_height(self):
        return float(self.height or 0)

    @cached_property
    def calculated_bar_width(self):
        return float(self.bar_width) * self.calculated_unit

    @cached_property
    def calculated_align(self):
        if self.align.upper() == 'LEFT':
            return e.FontAlign.LEFT
        elif self.align.upper() == 'CENTER':
            return e.FontAlign.CENTER
        elif self.align.upper() == 'RIGHT':
            return e.FontAlign().RIGHT

    def process(self, builder: Callable):
        return builder(e.Barcode) \
            .align(self.calculated_align) \
            .height(self.calculated_height) \
            .bar_width(self.calculated_bar_width) \
            .margin(*self.calculated_margin) \
            .code_set(self.code_set) \
            .value(self.value) \
            .draw()
