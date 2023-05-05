#!/bin/bash
command -v python3 || sudo dnf install python3 -y

python3 -m venv \
    ~/.virtualenvs/crosscompute-homepage
source \
    ~/.virtualenvs/crosscompute-homepage/bin/activate

bash setup.sh
