#!/usr/bin/env python3
import re
from argparse import ArgumentParser
from pathlib import Path
from time import sleep
from urllib.parse import urlparse as parse_uri

import httpx2
from bs4 import BeautifulSoup
from invisibleroads_macros_process import StoppableProcess
from invisibleroads_macros_web.port import find_open_port

from serve import load_configuration, serve_with


URL_PATTERN = re.compile(r'url\([\'"]?(.*?)[\'"]?\)')
SAVED_URIS = set()


def save(
        client, target_folder, relative_path, source_uri,
        *, is_recursive=False, is_binary=False):
    target_path = target_folder / relative_path.lstrip('/')
    target_path.parent.mkdir(parents=True, exist_ok=True)
    response = client.get(source_uri)
    response.raise_for_status()
    if is_binary:
        target_path.write_bytes(response.content)
        return
    html = response.text
    if is_recursive:
        uri_structure = parse_uri(source_uri)
        root_uri = uri_structure.scheme + '://' + uri_structure.netloc
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup.find_all('link'):
            if not (href := element.get('href')) or href.startswith('http'):
                continue
            save_asset(
                client, target_folder, root_uri, href,
                is_binary=href.endswith('.ico'))
        for element in soup.find_all('img'):
            src = element.get('src', element.get('data-src'))
            if not src or src.startswith('http'):
                continue
            save_asset(client, target_folder, root_uri, src)
        for relative_uri in URL_PATTERN.findall(html):
            save_asset(client, target_folder, root_uri, relative_uri)
    target_path.write_text(html)


def save_asset(
        client, target_folder, root_uri, relative_path, *, is_binary=True):
    if (uri := root_uri + '/' + relative_path.lstrip('/')) in SAVED_URIS:
        return
    SAVED_URIS.add(uri)
    save(client, target_folder, relative_path, uri, is_binary=is_binary)


def wait_for(client, uri, tries=30):
    for _ in range(tries):
        try:
            client.get(uri)
        except httpx2.ConnectError:
            sleep(1)
            continue
        return
    x = f'could not reach {uri}'
    raise SystemExit(x)


if __name__ == '__main__':
    a = ArgumentParser()
    a.add_argument('configuration_path', type=Path)
    a.add_argument('target_folder', type=Path)
    args = a.parse_args()
    args.port = find_open_port()
    args.is_production = True
    load_configuration(args.configuration_path)
    process = StoppableProcess(name='serve', target=serve_with, args=(args,))
    process.start()
    uri = f'http://localhost:{args.port}'
    with httpx2.Client(follow_redirects=True) as client:
        try:
            wait_for(client, uri)
            save(
                client, args.target_folder, 'index.html', uri,
                is_recursive=True)
        finally:
            process.stop()
