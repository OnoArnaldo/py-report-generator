from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from reportgen.elements import Line


def test_column(canvas):
    line1 = Line(canvas) \
        .parent_size(*pagesizes.A4) \
        .margin(cm) \
        .dashes(3, 6, 1) \
        .draw()

    line2 = line1.build_sibling(Line).margin(cm).draw()

    canvas.save()

    assert object.__getattribute__(canvas, 'log') == [
        ['canvas/saveState(..)', (), {}],
        ['canvas/setDash(..)', ((3, 6, 1),), {}],
        ['canvas/setLineWidth(..)', (1,), {}],
        ['canvas/line(..)',
         (28.346456692913385,
          28.346456692913385,
          538.5826771653544,
          28.346456692913385),
         {}],
        ['canvas/restoreState(..)', (), {}],
        ['canvas/saveState(..)', (), {}],
        ['canvas/setDash(..)', ([],), {}],
        ['canvas/setLineWidth(..)', (1,), {}],
        ['canvas/line(..)',
         (28.346456692913385, 86.03937007874015, 538.5826771653544, 86.03937007874015),
         {}],
        ['canvas/restoreState(..)', (), {}],
        ['canvas/save(..)', (), {}]
    ]
