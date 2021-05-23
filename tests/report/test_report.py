import os
from reportgen.report import Report
from ..utils import Ignore

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')


def assets(image):
    return os.path.join(ASSETS_DIR, image)


def test_report(canvas):
    report = Report(name='report001', unit='cm', page_size='A4', font='Courier 10 left')
    page = report.new_page(name='page001', margin='1')

    row1 = page.new_row(name='header001', margin='0 0 0.5 0', height='5', border='0')
    col01 = row1.new_column(name='col001', width='15', border='1', margin='0 0 0 0.2')
    txt01 = col01.new_text(name='txt001', font='Courier 7 left', margin='0 0.1', value='Company name:')
    txt02 = col01.new_text(name='txt002', margin='0 1 0 0.2', value='Arnaldo Ono')

    col02 = row1.new_column(name='col002', border='1', margin='0 0.2 0 0')
    img01 = col02.new_image(name='img001', value=assets('150.png'))

    row2 = page.new_row(name='withLines', margin='0', height='5', border='1')
    ln01 = row2.new_line(name='continuous', margin='0.5', stroke='1')
    ln02 = row2.new_line(name='dashed', margin='1', stroke='1', dashes='3 6 1')

    report.process(canvas)

    canvas.save()

    assert object.__getattribute__(canvas, 'log') == [
        ['canvas/roundRect(..)',
         (28.346456692913385,
          28.346456692913385,
          425.1968503937008,
          141.73228346456693,
          5.0,
          1),
         {}],
        ['canvas/saveState(..)', (), {}],
        ['canvas/setFont', ('Courier', 7, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 7'],
        ['canvas/drawString(..)',
         (31.181102362204726, 35.346456692913385, 'Company name:'),
         {}],
        ['canvas/restoreState(..)', (), {}],
        ['canvas/saveState(..)', (), {}],
        ['canvas/setFont', ('Courier', 10, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 10'],
        ['canvas/drawString(..)',
         (56.69291338582677, 45.346456692913385, 'Arnaldo Ono'),
         {}],
        ['canvas/restoreState(..)', (), {}],
        ['canvas/roundRect(..)',
         (464.88188976377955,
          28.346456692913385,
          102.04724409448826,
          141.73228346456693,
          5.0,
          1),
         {}],
        ['canvas/drawImage(..)',
         (Ignore,
          464.88188976377955,
          28.346456692913385,
          102.04724409448829,
          141.73228346456693),
         {'preserveAspectRatio': True}],
        ['canvas/roundRect(..)',
         (28.346456692913385,
          184.251968503937,
          538.5826771653544,
          141.73228346456693,
          5.0,
          1),
         {}],
        ['canvas/saveState(..)', (), {}],
        ['canvas/setDash(..)', ((),), {}],
        ['canvas/setLineWidth(..)', (1,), {}],
        ['canvas/line(..)',
         (42.519685039370074, 198.4251968503937, 552.7559055118111, 198.4251968503937),
         {}],
        ['canvas/restoreState(..)', (), {}],
        ['canvas/saveState(..)', (), {}],
        ['canvas/setDash(..)', ((3, 6, 1),), {}],
        ['canvas/setLineWidth(..)', (1,), {}],
        ['canvas/line(..)',
         (56.69291338582677, 241.9448818897638, 538.5826771653544, 241.9448818897638),
         {}],
        ['canvas/restoreState(..)', (), {}],
        ['canvas/showPage(..)', (), {}],
        ['canvas/save(..)', (), {}]
    ]
