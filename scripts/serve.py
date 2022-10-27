from argparse import ArgumentParser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from invisibleroads_macros_web.markdown import get_html_from_markdown
from ruamel.yaml import YAML
from watchfiles import run_process


PORT = 8000
BASE_FOLDER = Path(__file__).parents[1]
IMAGES_FOLDER = BASE_FOLDER / 'images'
# STYLES_FOLDER = BASE_FOLDER / 'styles'
TEMPLATES_FOLDER = BASE_FOLDER / 'templates'


app = FastAPI()
app.mount('/images', StaticFiles(directory=IMAGES_FOLDER), name='images')
# app.mount('/styles', StaticFiles(directory=STYLES_FOLDER), name='styles')
templates = Jinja2Templates(
    directory=TEMPLATES_FOLDER, trim_blocks=True, auto_reload=True)
configuration = {}


@app.get('/', response_class=HTMLResponse)
async def see_home(request: Request):
    return templates.TemplateResponse('index.html', configuration | {
        'request': request})


@app.get('/favicon.ico')
async def see_icon():
    return FileResponse(IMAGES_FOLDER / 'favicon.ico')


def serve_with(args):
    configuration.update(load_configuration(args.configuration_path))
    uvicorn.run(app, port=args.port, log_level='debug')


def load_configuration(path):
    yaml = YAML()
    with Path(path).open('rt') as f:
        c = yaml.load(f)
    ds = [c]
    while ds:
        d = ds.pop()
        for k, v in d.items():
            if isinstance(v, dict):
                ds.append(v)
            elif isinstance(v, list):
                ds.extend(v)
            elif k == 'description':
                d[k] = get_html_from_markdown(v)
    return c


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument('--port', metavar='X', default=PORT)
    a.add_argument('configuration_path')
    args = a.parse_args()
    run_process('.', target=serve_with, args=(args,))
