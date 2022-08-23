import uvicorn
from argparse import ArgumentParser

from fastapi import FastAPI


HOST = '127.0.0.1'
PORT = 8000


app = FastAPI()


@app.get('/')
def see_home():
    return {'Hello': 'World'}


def serve_with(args):
    uvicorn.run(app, port=args.port, log_level='debug')


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument(
        '--host', metavar='X', default=HOST)
    a.add_argument(
        '--port', metavar='X', default=PORT)
    args = a.parse_args()
    serve_with(args)
