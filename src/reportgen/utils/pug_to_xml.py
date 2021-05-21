import json
import os
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
from pypugjs.ext.jinja import PyPugJSExtension

asset_folder = ''


def _get_asset(fname):
    return os.path.join(asset_folder, fname)


def __ns(tag, ns):
    if isinstance(ns, dict) and ':' in tag:
        tag_ns, tag_name = tag.split(':')
        return '{' + ns.get(tag_ns, '') + '}' + tag_name
    return tag


def _get_namespace(data, path, ns=None):
    result = data
    for tag in path.split('/'):
        ns_tag = __ns(tag, ns)
        if (value := result.get(tag)) is not None:
            result = value
        elif (value := result.get(ns_tag)) is not None:
            result = value

    return result.get('$', result)


class Data:
    def __init__(self, data: [Dict, List, str]):
        self.data = data

    def __repr__(self):
        return f'Data({self.data!r})'

    def __eq__(self, other):
        return self.data == getattr(other, 'data', None)

    def __getattr__(self, item):
        data = self.data
        if isinstance(data, dict):
            if item in data:
                return Data(data[item])

            children = data.get('children', [])
            return Data([c[item] for c in children if item in c])
        elif isinstance(data, list) and len(data) == 1:
            data = data[0]
            if item in data:
                return Data(data[item])

            children = data.get('children', [])
            return Data([c[item] for c in children if item in c])

    def __getitem__(self, item):
        data = self.data
        if item == '$':
            if isinstance(data, str):
                return data
            elif isinstance(data, dict):
                return '\n'.join(data.get('children', []))
            elif isinstance(data, list):
                if len(data) == 1 and isinstance(data[0], dict):
                    return '\n'.join(data[0].get('children', []))
                return '\n'.join(data)
        elif item.startswith('@'):
            att_name = item[1:]
            if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
                return data[0].get('attributes', {}).get(att_name, '')
            return data.get('attributes', {}).get(att_name, '')
        elif item == '*' and isinstance(data, list):
            return [Data(d) for d in data]


def build_environment(*, template_dir, asset_dir):
    global asset_folder
    asset_folder = asset_dir

    return Environment(
        extensions=[PyPugJSExtension],
        loader=FileSystemLoader(template_dir),
        variable_start_string="{%#.-.**",
        variable_end_string="**.-.#%}",
    )


def build_renderer(jinja_env: Environment):
    def render(template, **kwargs):
        return jinja_env\
            .get_template(f'{template}.pug')\
            .render(enumerate=enumerate,
                    asset=_get_asset,
                    getNS=_get_namespace,
                    **kwargs)

    return render


def build_data(data: Dict) -> 'object':
    return Data(data)
