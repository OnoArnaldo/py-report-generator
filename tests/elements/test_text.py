from reportlab.lib import pagesizes
from reportlab.lib.units import cm
from reportgen.elements import Text, Column, Row
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
         (297.6377952755906, 20.0, 'This is the title'),
         {}],
        ['canvas/setFont', ('Courier', 10, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 10'],
        ['canvas/drawString(..)',
         (56.69291338582677, 86.69291338582677, 'Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawString(..)',
         (28.346456692913385, 179.73228346456693, 'Yet Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 10, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 10'],
        ['canvas/drawRightString(..)',
         (538.5826771653544, 274.7716535433071, 'Yet Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawRightString(..)',
         (566.9291338582677, 367.81102362204723, 'Yet Antoher line'),
         {}],
        ['canvas/setFont', ('Courier', 8, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 8'],
        ['canvas/drawRightString(..)',
         (269.2913385826772, 432.503937007874, 'Yet Antoher line'),
         {}]
    ]


def test_text_inside_box(canvas):
    row = Row(canvas).parent_size(*pagesizes.A4).margin(cm).stroke(0).draw()

    row1 = row.build_child(Row).height(5 * cm).stroke(1).draw()
    text1 = row1.build_child(Text).font('Courier', 12, FontAlign.LEFT).value('Line 001').draw()
    text2 = text1.build_sibling(Text).font('Courier', 20, FontAlign.LEFT).margin(cm).value('Line 002').draw()

    row2 = row1.build_sibling(Row).stroke(0).draw()
    col1 = row2.build_child(Column).width(6 * cm).stroke(1).draw()
    text1 = col1.build_child(Text).font('Courier', 12, FontAlign.LEFT).value('To the left').draw()
    text2 = text1.build_sibling(Text).font('Courier', 12, FontAlign.CENTER).value('To the centre').draw()
    text3 = text2.build_sibling(Text).font('Courier', 12, FontAlign.RIGHT).value('To the right').draw()

    col2 = col1.build_sibling(Column).width(6 * cm).stroke(1).draw()
    text1 = col2.build_child(Text).font('Courier', 12, FontAlign.LEFT).value('To the left').draw()
    text2 = text1.build_sibling(Text).font('Courier', 12, FontAlign.CENTER).value('To the centre').draw()
    text3 = text2.build_sibling(Text).font('Courier', 12, FontAlign.RIGHT).value('To the right').draw()

    col3 = col2.build_sibling(Column).stroke(1).draw()
    text1 = col3.build_child(Text).font('Courier', 12, FontAlign.LEFT).value('To the left').draw()
    text2 = text1.build_sibling(Text).font('Courier', 12, FontAlign.CENTER).value('To the centre').draw()
    text3 = text2.build_sibling(Text).font('Courier', 12, FontAlign.RIGHT).value('To the right').draw()

    canvas.save()

    assert object.__getattribute__(canvas, 'log') == [
        ['canvas/roundRect(..)',
         (28.346456692913385,
          28.346456692913385,
          538.5826771653544,
          141.73228346456693,
          5.0,
          1),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawString(..)',
         (28.346456692913385, 40.346456692913385, 'Line 001'),
         {}],
        ['canvas/setFont', ('Courier', 20, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 20'],
        ['canvas/drawString(..)',
         (56.69291338582677, 88.69291338582677, 'Line 002'),
         {}],
        ['canvas/roundRect(..)',
         (28.346456692913385,
          170.07874015748033,
          170.0787401574803,
          643.464566929134,
          5.0,
          1),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawString(..)',
         (28.346456692913385, 182.07874015748033, 'To the left'),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawCentredString(..)',
         (113.38582677165354, 194.07874015748033, 'To the centre'),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawRightString(..)',
         (198.4251968503937, 206.07874015748033, 'To the right'),
         {}],
        ['canvas/roundRect(..)',
         (198.4251968503937,
          170.07874015748033,
          170.0787401574803,
          643.464566929134,
          5.0,
          1),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawString(..)',
         (198.4251968503937, 182.07874015748033, 'To the left'),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawCentredString(..)',
         (283.46456692913387, 194.07874015748033, 'To the centre'),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawRightString(..)',
         (368.503937007874, 206.07874015748033, 'To the right'),
         {}],
        ['canvas/roundRect(..)',
         (368.503937007874,
          170.07874015748033,
          198.42519685039383,
          643.464566929134,
          5.0,
          1),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawString(..)',
         (368.503937007874, 182.07874015748033, 'To the left'),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawCentredString(..)',
         (467.71653543307093, 194.07874015748033, 'To the centre'),
         {}],
        ['canvas/setFont', ('Courier', 12, None), {}],
        ['canvas._fontname = Courier'],
        ['canvas._fontsize = 12'],
        ['canvas/drawRightString(..)',
         (566.9291338582678, 206.07874015748033, 'To the right'),
         {}],
        ['canvas/save(..)', (), {}]
    ]
