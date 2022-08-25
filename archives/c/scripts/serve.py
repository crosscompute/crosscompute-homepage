import operator
from pathlib import Path
from pyramid.events import NewRequest, subscriber

import yaml
from markdown import markdown
from pyramid.config import Configurator
from pyramid.response import FileResponse


@subscriber(NewRequest)
def reload_configuration(event):
    load_configuration(CONFIGURATION_PATH)


def index(request):
    metadata = find_item(
        CONFIGURATION['pages'], 'id', 'index',
        get_value=lambda item, key: item[key])
    return metadata


def load_configuration(configuration_path):
    configuration_path = Path(configuration_path)
    configuration_folder = configuration_path.parent
    with open(configuration_path, 'rt') as configuration_file:
        configuration = yaml.safe_load(configuration_file)
    for section in 'pages', 'posts':
        for d in configuration.get(section, []):
            process_dictionary(d['description'], configuration_folder)
    CONFIGURATION.update(configuration)
    return configuration


def process_dictionary(dictionary, configuration_folder):
    path = configuration_folder / dictionary['path']
    with open(path, 'rt') as f:
        text = f.read()
    if path.suffix == '.md':
        html = get_html_from_markdown(text, extensions=['tables'])
        dictionary['html'] = html
    dictionary['text'] = text


def _get_app():
    config.add_subscriber(reload_configuration, NewRequest)
    _configure_renderer_globals(config)


def _configure_renderer_globals(config):
    def update_renderer_globals():
        config.get_jinja2_environment().globals.update({
            'IMAGE_URI': '/images',
            'STYLE_URI': '/styles',
            'CONFIGURATION': CONFIGURATION,
        })

    config.action(None, update_renderer_globals)


def find_item(
        items, key, value, get_value=lambda item, key: getattr(item, key),
        normalize=lambda _: _, compare=operator.eq):
    normalized_value = normalize(value)

    def is_match(item):
        try:
            v = get_value(item, key)
        except KeyError:
            is_match = False
        else:
            normalized_v = normalize(v)
            is_match = compare(normalized_value, normalized_v)
        return is_match

    return next(filter(is_match, items))


def get_html_from_markdown(text, extensions=None):
    html = markdown(text, extensions=extensions)
    if '</p>\n<p>' not in html:
        html = html.removeprefix('<p>')
        html = html.removesuffix('</p>')
    return html


DATASETS_FOLDER = BASE_FOLDER / 'datasets'
CONFIGURATION_PATH = DATASETS_FOLDER / 'configuration.yml'
CONFIGURATION = {}
