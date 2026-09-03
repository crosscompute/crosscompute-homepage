from argparse import ArgumentParser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from markdown2 import markdown
from ruamel.yaml import YAML
from watchfiles import run_process


PORT = 8000
BASE_FOLDER = Path(__file__).parents[1]
ASSETS_FOLDER = BASE_FOLDER / 'assets'
MARKDOWN_EXTRAS = ['target-blank-links']


app = FastAPI()
app.mount('/assets', StaticFiles(directory=ASSETS_FOLDER), name='assets')
env = Environment(
    loader=FileSystemLoader(ASSETS_FOLDER),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True)
templates = Jinja2Templates(
    env=env)
configuration = {}


@app.get('/', response_class=HTMLResponse)
async def see_home(request: Request):
    return templates.TemplateResponse(request, 'index.html', configuration)


@app.get('/favicon.{extension}')
async def see_icon(extension: str):
    if extension not in ('ico', 'svg'):
        raise HTTPException(404)
    return FileResponse(ASSETS_FOLDER / f'favicon.{extension}')


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
        for k, v in d.copy().items():
            if isinstance(v, dict):
                ds.append(v)
            elif isinstance(v, list):
                ds.extend(x for x in v if isinstance(x, dict))
            elif k.endswith('_markdown') and isinstance(v, str):
                d[k.removesuffix('_markdown') + '_html'] = markdown(
                    v, extras=MARKDOWN_EXTRAS)
    return c


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument('--port', metavar='X', type=int, default=PORT)
    a.add_argument('configuration_path', type=Path)
    args = a.parse_args()
    run_process(
        BASE_FOLDER, args.configuration_path, target=serve_with,
        args=(args,))
