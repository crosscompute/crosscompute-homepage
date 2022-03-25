command -v python3.9 || sudo dnf install python39 -y

python3.9 -m venv \
    ~/.virtualenvs/crosscompute-homepage
source \
    ~/.virtualenvs/crosscompute-homepage/bin/activate

pip install -U \
    beautifulsoup4 \
    crosscompute \
    markdown \
    pip \
    pyramid \
    pyyaml \
    requests
