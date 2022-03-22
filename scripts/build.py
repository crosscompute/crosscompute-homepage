import requests
from argparse import ArgumentParser
from crosscompute.macros.process import StoppableProcess
from crosscompute.macros.web import find_open_port
from pathlib import Path
from time import sleep

from serve import load_configuration, serve_with


def save(target_path, source_uri):
    target_path.parent.mkdir(exist_ok=True)
    while True:
        try:
            response = requests.get(source_uri)
        except requests.exceptions.ConnectionError:
            sleep(1)
            continue
        break
    with open(target_path, 'wt') as f:
        f.write(response.content.decode())


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument('configuration_path')
    a.add_argument('target_folder')
    args = a.parse_args()
    args.host = '127.0.0.1'
    args.port = find_open_port()
    args.is_production = True
    load_configuration(args.configuration_path)
    process = StoppableProcess(name='serve', target=serve_with, args=(args,))
    process.start()
    uri = f'http://localhost:{args.port}'
    target_folder = Path(args.target_folder)
    try:
        save(target_folder / 'index.html', uri)
    finally:
        process.stop()
