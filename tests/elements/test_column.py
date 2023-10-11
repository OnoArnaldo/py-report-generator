# pylint: disable=unused-variable
from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from reportgen.elements import Column


def test_column(canvas):
    col1 = Column(canvas).parent_size(*pagesizes.A4).margin(cm).width(5 * cm).draw()

    col11: Column = col1.build_child(Column).margin(0.5 * cm).width(2 * cm).draw()
    col12: Column = col11.build_sibling(Column).margin(0.2 * cm).width(2 * cm).draw()

    col2: Column = col1.build_sibling(Column).margin(2 * cm).width(5 * cm).draw()
    col21: Column = col2.build_child(Column).margin(cm).draw()

    canvas.save()

    assert object.__getattribute__(canvas, 'log') == [
        [
            'canvas/roundRect(..)',
            (28.346456692913385, 28.346456692913385, 141.73228346456693, 785.196850393701, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (42.519685039370074, 42.519685039370074, 56.69291338582677, 756.8503937007875, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (119.05511811023622, 34.01574803149606, 45.35433070866142, 773.8582677165356, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (255.1181102362205, 56.69291338582677, 141.73228346456693, 728.5039370078741, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (283.46456692913387, 85.03937007874015, 85.03937007874016, 671.8110236220474, 5.0, 1),
            {},
        ],
        ['canvas/save(..)', (), {}],
    ]
