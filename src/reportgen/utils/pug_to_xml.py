import os
from jinja2 import Environment, FileSystemLoader
from pypugjs.ext.jinja import PyPugJSExtension

asset_folder = ''


def _get_asset(fname):
    return os.path.join(asset_folder, fname)


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
                    **kwargs)

    return render
