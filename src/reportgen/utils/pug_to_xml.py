import os
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
