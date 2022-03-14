import yaml
from argparse import ArgumentParser
from markdown import markdown
from pathlib import Path
from pyramid.config import Configurator
from wsgiref.simple_server import make_server


def index(request):
    return {
        'title_text': 'CrossCompute Updates',
        'articles': CONFIGURATION['articles'],
    }


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
    return configuration


def _get_app(is_production):
    settings = {
        'jinja2.trim_blocks': True,
    }
    if not is_production:
        settings['pyramid.reload_templates'] = True
    with Configurator(settings=settings) as config:
        config.add_route('index', '/')
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path(str(TEMPLATES_FOLDER))
        config.add_static_view(name='images', path=str(IMAGES_FOLDER))
        config.add_static_view(name='styles', path=str(STYLES_FOLDER))
        config.add_view(
            index, route_name='index', renderer='index.jinja2')
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


BASE_FOLDER = Path(__file__).parents[1]
IMAGES_FOLDER = BASE_FOLDER / 'images'
STYLES_FOLDER = BASE_FOLDER / 'styles'
TEMPLATES_FOLDER = BASE_FOLDER / 'templates'
CONFIGURATION = {}


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument('configuration_path')
    a.add_argument('--production', dest='is_production', action='store_true')
    args = a.parse_args()
    CONFIGURATION.update(load_configuration(args.configuration_path))
    app = _get_app(args.is_production)
    server = make_server('0.0.0.0', 8000, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
