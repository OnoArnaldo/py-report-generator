import os
from .utils import pug_to_xml as pug, xml_to_dict as xml
from . import report as r


class Parser:
    def __init__(self, template_dir, data_dir, asset_dir):
        self.template_dir = template_dir
        self.data_dir = data_dir
        self.asset_dir = asset_dir

        env = pug.build_environment(template_dir=self.template_dir, asset_dir=self.asset_dir)
        self.render = pug.build_renderer(env)

    def __call__(self, template, data):
        data = xml.from_file(os.path.join(self.data_dir, data))
        report_xml = self.render(template, data=data)
        report_dict = xml.from_string(report_xml, 'abdera')

        k, v = report_dict.popitem()
        att = v.get('attributes', {})

        if k.upper() == 'REPORT':
            e = r.Report(name=att.get('id', ''),
                         page_size=att.get('page-size', ''),
                         unit=att.get('unit', ''),
                         font=att.get('font', ''))

            self.process(v.get('children', []), e)

            return e

    def process(self, data, parent):
        if isinstance(data, list):
            for el in data:
                k, v = el.popitem()
                att = v.get('attributes', {}) if isinstance(v, dict) else {}

                if k.upper() == 'PAGE':
                    new_el = parent.new_page(name=att.get('id', ''),
                                             font=att.get('font', ''),
                                             margin=att.get('margin', ''))

                    self.process(v.get('children', []), new_el)

                elif k.upper() == 'ROW':
                    new_el = parent.new_row(name=att.get('id', ''),
                                            height=att.get('height', ''),
                                            margin=att.get('margin', ''),
                                            border=att.get('border', ''),
                                            font=att.get('font', ''))

                    self.process(v.get('children', []), new_el)

                elif k.upper() == 'COLUMN':
                    new_el = parent.new_column(name=att.get('id', ''),
                                               width=att.get('width', ''),
                                               margin=att.get('margin', ''),
                                               border=att.get('border', ''),
                                               font=att.get('font', ''))

                    self.process(v.get('children', []), new_el)

                elif k.upper() == 'TEXT':
                    if isinstance(v, dict):
                        v = v.get('children', [''])[0]

                    parent.new_text(name=att.get('id', ''),
                                    font=att.get('font', ''),
                                    margin=att.get('margin', ''),
                                    value=str(v))

                elif k.upper() == 'IMAGE':
                    if isinstance(v, dict):
                        v = v.get('children', [''])[0]

                    parent.new_image(name=att.get('id', ''), value=str(v))
