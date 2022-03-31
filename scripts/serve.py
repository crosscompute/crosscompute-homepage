import operator
from argparse import ArgumentParser
from pathlib import Path
from pyramid.events import NewRequest, subscriber
from wsgiref.simple_server import make_server

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


def see_icon(request):
    return FileResponse(IMAGES_FOLDER / 'favicon.ico')


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


def serve_with(args):
    app = _get_app()
    server = make_server(args.host, args.port, app)
    print(f'http://localhost:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def _get_app():
    settings = {
        'jinja2.trim_blocks': True,
        'pyramid.reload_templates': True,
    }
    with Configurator(settings=settings) as config:
        config.add_route('index', '/')
        config.add_route('icon', '/favicon.ico')
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path(str(TEMPLATES_FOLDER))
        config.add_static_view(name='images', path=str(IMAGES_FOLDER))
        config.add_static_view(name='styles', path=str(STYLES_FOLDER))
        config.add_view(index, route_name='index', renderer='index.jinja2')
        config.add_view(see_icon, route_name='icon')
        config.add_subscriber(reload_configuration, NewRequest)
        _configure_renderer_globals(config)
        app = config.make_wsgi_app()
    return app


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


HOST = '127.0.0.1'
PORT = 8000
BASE_FOLDER = Path(__file__).parents[1]
DATASETS_FOLDER = BASE_FOLDER / 'datasets'
IMAGES_FOLDER = BASE_FOLDER / 'images'
STYLES_FOLDER = BASE_FOLDER / 'styles'
TEMPLATES_FOLDER = BASE_FOLDER / 'templates'
CONFIGURATION_PATH = DATASETS_FOLDER / 'configuration.yml'
CONFIGURATION = {}


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument(
        '--host', metavar='X', default=HOST)
    a.add_argument(
        '--port', metavar='X', default=PORT)
    args = a.parse_args()
    serve_with(args)
