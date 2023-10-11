import typing as _
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from pypugjs.ext.jinja import PyPugJSExtension

asset_folder = ''


def _get_asset(fname: str) -> Path:
    return Path(asset_folder, fname)


def _data_with_namespace(data: 'Data', namespace: _.Dict) -> 'DataWithNS':
    return DataWithNS(data.data, namespace)


class Data:
    def __init__(self, data: _.Dict | _.List | str):
        self.data = data

    def __repr__(self) -> str:
        return f'Data({self.data!r})'

    def __eq__(self, other: 'Data') -> bool:
        return self.data == getattr(other, 'data', None)

    def __getattr__(self, item: _.Any) -> 'Data':
        data = self.data
        if isinstance(data, dict):
            if item in data:
                return Data(data[item])

            children = data.get('children', [])
            return Data([c[item] for c in children if item in c])
        if isinstance(data, list) and len(data) == 1:
            data = data[0]
            if item in data:
                return Data(data[item])

            children = data.get('children', [])
            return Data([c[item] for c in children if item in c])
        return Data('')

    def __getitem__(self, item: str) -> str | list['Data'] | None:
        if item == '$':
            return self.get_value()
        if item.startswith('@'):
            return self.get_attribute(item)
        if item == '*':
            return self.get_items()

        return None

    def get_value(self) -> str:
        data = self.data
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            return '\n'.join(data.get('children', []))
        if isinstance(data, list):
            if len(data) == 1 and isinstance(data[0], dict):
                return '\n'.join(data[0].get('children', []))
            return '\n'.join(data)
        return ''

    def get_attribute(self, item: str) -> str:
        data = self.data
        att_name = item[1:]
        if isinstance(data, list):
            if len(data) == 1 and isinstance(data[0], dict):
                return data[0].get('attributes', {}).get(att_name, '')
            return ''
        if isinstance(data, str):
            return ''
        return data.get('attributes', {}).get(att_name, '')

    def get_items(self) -> list:
        data = self.data
        return [Data(d) for d in data] if isinstance(data, list) else []


class DataWithNS(Data):
    def __init__(self, data: dict | list | str, ns: _.Dict):
        super().__init__(data)
        self.ns = ns

    def __getattr__(self, item: str) -> 'Data':
        name = item
        if '__' in item:
            ns, name = item.split('__')
            name = '{' + self.ns.get(ns, '') + '}' + name

        ret = super().__getattr__(name)
        return DataWithNS(ret.data, self.ns)

    def __getitem__(self, item: str) -> str | list['Data']:
        ret = super().__getitem__(item)
        if isinstance(ret, list):
            return [DataWithNS(i.data, self.ns) for i in ret]
        return ret


def build_environment(*, template_dir: Path, asset_dir: Path) -> Environment:
    global asset_folder
    asset_folder = asset_dir

    return Environment(
        extensions=[PyPugJSExtension],
        loader=FileSystemLoader(template_dir),
        variable_start_string="{%#.-.**",
        variable_end_string="**.-.#%}",
    )


def build_renderer(jinja_env: Environment) -> _.Callable:
    def render(template, **kwargs):
        return jinja_env.get_template(f'{template}.pug').render(
            enumerate=enumerate, asset=_get_asset, dataNS=_data_with_namespace, **kwargs
        )

    return render


def build_data(data: _.Dict | _.List | str) -> 'Data':
    return Data(data)
