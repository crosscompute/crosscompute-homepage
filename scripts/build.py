import re
from argparse import ArgumentParser
from pathlib import Path
from time import sleep
from urllib.parse import urlparse as parse_uri

import requests
from bs4 import BeautifulSoup
from invisibleroads_macros_process import StoppableProcess
from invisibleroads_macros_web.port import find_open_port

from serve import load_configuration, serve_with


def save(
        target_folder, relative_path, source_uri, is_recursive=False,
        is_binary=False):
    target_path = target_folder / relative_path.lstrip('/')
    target_path.parent.mkdir(exist_ok=True)
    while True:
        try:
            response = requests.get(source_uri)
        except requests.exceptions.ConnectionError:
            sleep(1)
            continue
        break
    if is_binary:
        with target_path.open('wb') as f:
            f.write(response.content)
        return
    html = response.content.decode()
    if is_recursive:
        uri_structure = parse_uri(source_uri)
        root_uri = uri_structure.scheme + '://' + uri_structure.netloc
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.find_all('link'):
            link_href = element.get('href')
            if not link_href or link_href.startswith('http'):
                continue
            uri = root_uri + '/' + link_href
            is_binary = uri.endswith('.ico')
            save(target_folder, link_href, uri, is_binary=is_binary)
        for element in soup.find_all('img'):
            img_src = element.get('src', element.get('data-src'))
            if not img_src or img_src.startswith('http'):
                continue
            uri = root_uri + '/' + img_src
            save(target_folder, img_src, uri, is_binary=True)
        for relative_uri in URL_PATTERN.findall(html):
            uri = root_uri + relative_uri
            save(target_folder, relative_uri.lstrip('/'), uri, is_binary=True)
    with target_path.open('wt') as f:
        f.write(html)


URL_PATTERN = re.compile(r'url\((.*)\)')


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument('configuration_path')
    a.add_argument('target_folder')
    args = a.parse_args()
    args.port = find_open_port()
    args.is_production = True
    configuration_path = args.configuration_path
    load_configuration(configuration_path)
    process = StoppableProcess(name='serve', target=serve_with, args=(args,))
    process.start()
    uri = f'http://localhost:{args.port}'
    folder = Path(args.target_folder)
    try:
        save(folder, 'index.html', uri, is_recursive=True)
        # save(folder, 'favicon.ico', uri + '/favicon.ico', is_binary=True)
    finally:
        process.stop()
