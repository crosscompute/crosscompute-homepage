from argparse import ArgumentParser

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


def serve_with(args):
    pass


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument(
        '--host', metavar='X', default=HOST)
    a.add_argument(
        '--port', metavar='X', default=PORT)
    args = a.parse_args()
    serve_with(args)
