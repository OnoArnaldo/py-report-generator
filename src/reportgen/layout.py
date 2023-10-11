import typing as _
from pathlib import Path
from .utils import pug_to_xml as pug, xml_to_dict as xml
from . import report as r


class Parser:
    def __init__(self, template_dir: Path, data_dir: Path, asset_dir: Path):
        self.template_dir = template_dir
        self.data_dir = data_dir
        self.asset_dir = asset_dir

        env = pug.build_environment(template_dir=self.template_dir, asset_dir=self.asset_dir)
        self.render = pug.build_renderer(env)

    def __call__(self, template: str, data: str, **renderer_args) -> r.Report:
        data = xml.from_file(Path(self.data_dir, data), 'abdera')
        data = pug.build_data(data)

        report_xml = self.render(template, data=data, **renderer_args)
        report_dict = xml.from_string(report_xml, 'abdera')

        k, v = report_dict.popitem()

        if k.upper() != 'REPORT':
            raise Exception('No report node has been found.')

        att = v.get('attributes', {})
        e = r.Report(
            name=att.get('id', ''),
            page_size=att.get('page-size', ''),
            unit=att.get('unit', ''),
            font=att.get('font', ''),
        )

        self.process(v.get('children', []), e)

        return e

    def process(self, data: list, parent: r.BaseT) -> _.NoReturn:
        if isinstance(data, list):
            for el in data:
                k, v = el.popitem()
                att = v.get('attributes', {}) if isinstance(v, dict) else {}

                if k.upper() == 'PAGE':
                    new_el = parent.new_page(
                        name=att.get('id', ''), font=att.get('font', ''), margin=att.get('margin', '')
                    )

                    self.process(v.get('children', []), new_el)

                elif k.upper() == 'ROW':
                    new_el = parent.new_row(
                        name=att.get('id', ''),
                        height=att.get('height', ''),
                        margin=att.get('margin', ''),
                        border=att.get('border', ''),
                        font=att.get('font', ''),
                    )

                    self.process(v.get('children', []), new_el)

                elif k.upper() == 'COLUMN':
                    new_el = parent.new_column(
                        name=att.get('id', ''),
                        width=att.get('width', ''),
                        margin=att.get('margin', ''),
                        border=att.get('border', ''),
                        font=att.get('font', ''),
                    )

                    self.process(v.get('children', []), new_el)

                elif k.upper() == 'TEXT':
                    if isinstance(v, dict):
                        v = v.get('children', [''])[0]

                    parent.new_text(
                        name=att.get('id', ''), font=att.get('font', ''), margin=att.get('margin', ''), value=str(v)
                    )

                elif k.upper() == 'IMAGE':
                    if isinstance(v, dict):
                        v = v.get('children', [''])[0]

                    parent.new_image(name=att.get('id', ''), value=str(v))

                elif k.upper() == 'LINE':
                    parent.new_line(
                        name=att.get('id', ''),
                        margin=att.get('margin', ''),
                        stroke=att.get('stroke', ''),
                        dashes=att.get('dashes', ''),
                    )

                elif k.upper() == 'BARCODE':
                    if isinstance(v, dict):
                        v = v.get('children', [''])[0]

                    parent.new_barcode(
                        name=att.get('id', ''),
                        margin=att.get('margin', ''),
                        bar_width=att.get('bar-width', ''),
                        height=att.get('height', ''),
                        align=att.get('align', ''),
                        code_set=att.get('code-set', ''),
                        value=v,
                    )
