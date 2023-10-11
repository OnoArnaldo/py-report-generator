# pylint: disable=unused-variable
from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from reportgen.elements import Row


def test_row(canvas):
    row1: Row = Row(canvas).parent_size(*pagesizes.A4).margin(cm).height(5 * cm).draw()

    row11: Row = row1.build_child(Row).margin(0.5 * cm).height(2 * cm).draw()
    row12: Row = row11.build_sibling(Row).margin(0.2 * cm).height(2 * cm).draw()

    row2: Row = row1.build_sibling(Row).margin(2 * cm).height(5 * cm).draw()
    row21: Row = row2.build_child(Row).margin(cm).draw()

    canvas.save()

    assert object.__getattribute__(canvas, 'log') == [
        [
            'canvas/roundRect(..)',
            (28.346456692913385, 28.346456692913385, 538.5826771653544, 141.73228346456693, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (42.519685039370074, 42.519685039370074, 510.23622047244106, 56.69291338582677, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (34.01574803149606, 119.05511811023622, 527.244094488189, 45.35433070866142, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (56.69291338582677, 255.1181102362205, 481.8897637795276, 141.73228346456693, 5.0, 1),
            {},
        ],
        [
            'canvas/roundRect(..)',
            (85.03937007874015, 283.46456692913387, 425.19685039370074, 85.03937007874016, 5.0, 1),
            {},
        ],
        ['canvas/save(..)', (), {}],
    ]
