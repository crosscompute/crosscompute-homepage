from argparse import ArgumentParser
from pathlib import Path
from wsgiref.simple_server import make_server

import yaml
from markdown import markdown
from pyramid.config import Configurator
from pyramid.response import FileResponse


def index(request):
    return {
        'title_text': 'CrossCompute',
        'page_description': (
            'CrossCompute provides infrastructure for hosting analytics '
            'content that organizations can license to customers.'),
        'articles': CONFIGURATION['articles'],
    }


def see_icon(request):
    return FileResponse(IMAGES_FOLDER / 'favicon.ico')


def load_configuration(configuration_path):
    configuration_path = Path(configuration_path)
    configuration_folder = configuration_path.parent
    with open(configuration_path, 'rt') as configuration_file:
        configuration = yaml.safe_load(configuration_file)
    for article_dictionary in configuration.get('articles', []):
        description_dictionary = article_dictionary['description']
        description_path = configuration_folder / description_dictionary[
            'path']
        with open(description_path, 'rt') as description_file:
            description_text = description_file.read()
        description_html = markdown(description_text)
        description_dictionary['html'] = description_html
    CONFIGURATION.update(configuration)
    return configuration


def serve_with(args):
    app = _get_app(args.is_production)
    server = make_server(args.host, args.port, app)
    print(f'http://localhost:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


def _get_app(is_production):
    settings = {
        'jinja2.trim_blocks': True,
    }
    if not is_production:
        settings['pyramid.reload_templates'] = True
    with Configurator(settings=settings) as config:
        config.add_route('index', '/')
        config.add_route('icon', '/favicon.ico')
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path(str(TEMPLATES_FOLDER))
        config.add_static_view(name='images', path=str(IMAGES_FOLDER))
        config.add_static_view(name='styles', path=str(STYLES_FOLDER))
        config.add_view(index, route_name='index', renderer='index.jinja2')
        config.add_view(see_icon, route_name='icon')
        _configure_renderer_globals(config)
        app = config.make_wsgi_app()
    return app


def _configure_renderer_globals(config):
    def update_renderer_globals():
        config.get_jinja2_environment().globals.update({
            'IMAGE_URI': '/images',
            'STYLE_URI': '/styles',
        })

    config.action(None, update_renderer_globals)


HOST = '127.0.0.1'
PORT = 8000
BASE_FOLDER = Path(__file__).parents[1]
IMAGES_FOLDER = BASE_FOLDER / 'images'
STYLES_FOLDER = BASE_FOLDER / 'styles'
TEMPLATES_FOLDER = BASE_FOLDER / 'templates'
CONFIGURATION = {}


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument(
        'configuration_path')
    a.add_argument(
        '--host', metavar='X', default=HOST)
    a.add_argument(
        '--port', metavar='X', default=PORT)
    a.add_argument(
        '--production', dest='is_production', action='store_true')
    args = a.parse_args()
    load_configuration(args.configuration_path)
    serve_with(args)
