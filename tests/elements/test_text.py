from pytest import approx
from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from reportgen.elements import Text, Column
from reportgen.enums import FontAlign


def test_text(canvas):
    text1 = Text(canvas) \
        .parent_size(*pagesizes.A4) \
        .font('Courier', 20, FontAlign.CENTER) \
        .value('This is the title') \
        .draw()

    text2: Text = text1.build_sibling(Text) \
        .font('Courier', 10, FontAlign.LEFT) \
        .margin(2 * cm) \
        .value('Antoher line') \
        .draw()

    text3: Text = text2.build_sibling(Text) \
        .font('Courier', 8, FontAlign.LEFT) \
        .margin(cm) \
        .value('Yet Antoher line') \
        .draw()

    text4: Text = text3.build_sibling(Text) \
        .font('Courier', 10, FontAlign.RIGHT) \
        .margin(2 * cm) \
        .value('Yet Antoher line') \
        .draw()

    text5: Text = text4.build_sibling(Text) \
        .font('Courier', 8, FontAlign.RIGHT) \
        .margin(cm) \
        .value('Yet Antoher line') \
        .draw()

    w, h = pagesizes.A4
    text6: Text = text5.build_sibling(Text) \
        .font('Courier', 8, FontAlign.RIGHT) \
        .margin(cm) \
        .parent_size(w / 2, text5.sibling.size.height) \
        .value('Yet Antoher line') \
        .draw()

    assert object.__getattribute__(canvas, 'log') == [
        ['canvas/setFont', ('Courier', 20, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 20'],
        ['canvas/drawCentredString(..)',
         (297.6377952755906, 0, 'This is the title'),
         {}],
        ['canvas/setFont', ('Courier', 10, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 10'],
        ['canvas/drawString(..)',
         (56.69291338582677, 76.69291338582677, 'Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawString(..)',
         (28.346456692913385, 171.73228346456693, 'Yet Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 10, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 10'],
        ['canvas/drawRightString(..)',
         (538.5826771653544, 264.7716535433071, 'Yet Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawRightString(..)',
         (566.9291338582677, 359.81102362204723, 'Yet Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawRightString(..)',
         (269.2913385826772, 424.503937007874, 'Yet Antoher line'),
         {}]
    ]


def test_text_inside_box(canvas):
    col1 = Column(canvas) \
        .parent_size(*pagesizes.A4) \
        .margin(0.2 * cm) \
        .width(6 * cm) \
        .draw()
    col2 = col1.build_sibling(Column).width(6 * cm).margin(0.2 * cm).draw()
    col3 = col2.build_sibling(Column).margin(0.2 * cm).draw()

    txt1 = col1.build_child(Text) \
        .font('Courier', 8, FontAlign.LEFT) \
        .margin(cm) \
        .value('To the left') \
        .draw()

    txt2 = col2.build_child(Text) \
        .font('Courier', 8, FontAlign.CENTER) \
        .margin(cm) \
        .value('To the right') \
        .draw()

    txt3 = col3.build_child(Text) \
        .font('Courier', 8, FontAlign.RIGHT) \
        .margin(cm) \
        .value('To the center') \
        .draw()

    canvas.save()

    assert object.__getattribute__(canvas, 'log') == [
        ['canvas/roundRect(..)',
         (5.669291338582678,
          5.669291338582678,
          170.0787401574803,
          830.5511811023623,
          5.0,
          1),
         {}],
        ['canvas/roundRect(..)',
         (187.08661417322833,
          5.669291338582678,
          170.0787401574803,
          830.5511811023623,
          5.0,
          1),
         {}],
        ['canvas/roundRect(..)',
         (368.503937007874,
          5.669291338582678,
          221.1023622047245,
          830.5511811023623,
          5.0,
          1),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawString(..)',
         (34.01574803149606, 34.01574803149606, 'To the left'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawCentredString(..)',
         (272.1259842519685, 34.01574803149606, 'To the right'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawRightString(..)',
         (561.2598425196851, 34.01574803149606, 'To the center'),
         {}],
        ['canvas/save(..)', (), {}]
    ]
