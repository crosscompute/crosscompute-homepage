from argparse import ArgumentParser
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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


@app.get('/', response_class=HTMLResponse)
async def see_home(request: Request):
    widgets = [{
        'name': 'Widget A',
        'description': 'Description for Widget A',
        'link_uri': 'https://www.interestingeverything.com/2013/03/07/tree-frog-amphibian-climber',
        'image_uri': 'https://i0.wp.com/www.interestingeverything.com/wp-content/uploads/2013/02/red-eyed-tree-frog.png?w=500&ssl=1',
        'video_uri': 'https://youtu.be/z0-Zi5ngQQw',
    }, {
        'name': 'Widget B',
        'description': 'Description for Widget B',
        'link_uri': 'https://www.interestingeverything.com/2013/03/07/tree-frog-amphibian-climber',
        'image_uri': 'https://i0.wp.com/www.interestingeverything.com/wp-content/uploads/2013/02/red-eyed-tree-frog.png?w=500&ssl=1',
        'video_uri': 'https://youtu.be/z0-Zi5ngQQw',
    }, {
        'name': 'Widget C',
        'description': 'Description for Widget C',
        'link_uri': 'https://www.interestingeverything.com/2013/03/07/tree-frog-amphibian-climber',
        'image_uri': 'https://i0.wp.com/www.interestingeverything.com/wp-content/uploads/2013/02/red-eyed-tree-frog.png?w=500&ssl=1',
        'video_uri': 'https://youtu.be/z0-Zi5ngQQw',
    }, {
        'name': 'Widget D',
        'description': 'Description for Widget D',
        'link_uri': 'https://www.interestingeverything.com/2013/03/07/tree-frog-amphibian-climber',
        'image_uri': 'https://i0.wp.com/www.interestingeverything.com/wp-content/uploads/2013/02/red-eyed-tree-frog.png?w=500&ssl=1',
        'video_uri': 'https://youtu.be/z0-Zi5ngQQw',
    }]
    websites = [{
        'name': 'Website A',
        'description': 'Description for Website A',
        'link_uri': 'https://www.interestingeverything.com/2013/03/07/tree-frog-amphibian-climber',
        'image_uri': 'https://i0.wp.com/www.interestingeverything.com/wp-content/uploads/2013/02/red-eyed-tree-frog.png?w=500&ssl=1',
        'video_uri': 'https://youtu.be/z0-Zi5ngQQw',
    }, {
        'name': 'Website B',
        'description': 'Description for Website B',
        'link_uri': 'https://www.interestingeverything.com/2013/03/07/tree-frog-amphibian-climber',
        'image_uri': 'https://i0.wp.com/www.interestingeverything.com/wp-content/uploads/2013/02/red-eyed-tree-frog.png?w=500&ssl=1',
        'video_uri': 'https://youtu.be/z0-Zi5ngQQw',
    }, {
        'name': 'Website C',
        'description': 'Description for Website C',
        'link_uri': 'https://www.interestingeverything.com/2013/03/07/tree-frog-amphibian-climber',
        'image_uri': 'https://i0.wp.com/www.interestingeverything.com/wp-content/uploads/2013/02/red-eyed-tree-frog.png?w=500&ssl=1',
        'video_uri': 'https://youtu.be/z0-Zi5ngQQw',
    }]
    return templates.TemplateResponse('index.html', {
        'request': request,
        'widgets': widgets,
        'websites': websites,
    })


@app.get('/favicon.ico')
async def see_icon():
    return FileResponse(IMAGES_FOLDER / 'favicon.ico')


def serve_with(args):
    uvicorn.run('serve:app', port=args.port, log_level='debug', reload=True)


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument('--port', metavar='X', default=PORT)
    args = a.parse_args()
    serve_with(args)
