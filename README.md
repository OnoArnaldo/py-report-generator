# Report Generator

This library helps to generate pdf report using a template with pugjs syntax and xml data.

# Installation

```shell
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install git+https://github.com/OnoArnaldo/py-report-generator.git
```

In case this project is still private, use the command below:

```shell
pip install git+ssh://git@github.com/OnoArnaldo/py-report-generator.git
```

# Usage

## Templates

The template uses pugjs syntax, and is processed with Jinja engine.

Example:
```jade
report#report-name(page-size="A4" unit="cm" font="Courier 10 left")
  page(margin="1")
    row(height="2" border="1")
      text= data.invoice.company.name['$']
    row#spacer(height="0.5")
    each line in data.invoice.item['*']
      row(height="2" border="1")
        text #{line.name['$']} - #{line.qty['$']} - #{line.price['$']}
```

The template can have the following structure:

```jade
report#report-id(page-size unit font)
  page#page-id(margin font)
    row#row-id(margin font border height)
    column#column-id(margin font border width)
    text#text-id(margin font) value #{withVariables}
    image#image-id(margin) fileName
```

> Note that:
> 
> `Report` can have multiple pages, and only `pages`
> 
> `Page`, `row` and `column` can have multiples `row`, `column`, `text` and `image`

> For more complex example, please go to the end of this document 


## XML data

The data is a xml file.

Example:
```xml
<invoice>
    <company>
        <name>The Company Name</name>
    </company>
    <item>
        <name>Item01</name>
        <qty>10</qty>
        <price>1000</price>
    </item>
    <item>
        <name>Item02</name>
        <qty>20</qty>
        <price>2000</price>
    </item>
    <item>
        <name>Item03</name>
        <qty>30</qty>
        <price>3000</price>
    </item>
</invoice>
```

# The code

A very simple implementation would be as below.

```python
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportgen.layout import Parser

parse = Parser(template_dir='/templates', data_dir='/data', asset_dir='/assets')

canvas = Canvas('filename.pdf', pagesize=A4, bottomup=0)
report = parse('invoiceLayout', 'invoice001.xml')
report.process(canvas)
canvas.save()
```

# Complex example

The reportgen will send the xml data to the template using the variable `data`.

You can chain the tags separated by `.` to reach specific value.
It has to finish with `['$']` to retrieve the value inside the tag.

example:
```jade
report
    page
        text= data.root.field['$']
```

To retrieve an attribute value, use `['@AttributeName']`.

example:
```jade
report
    page
        text= data.root.field['@id']
```

And to iterate through multiple elements, use `['*']`.

example:
```jade
report
    page
        each item in data.root.item['*']
            text= item.name['$']
```

Pugjs allows the creation of variables, which can be useful with the data structure.

example:
```jade
- var compAddr = data.company.address

report
    page
        text= compAddr.line1['$']
        text= compAddr.city['$']
```