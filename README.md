# CrossCompute Homepage

## Installation

Add a deploy key to https://github.com/crosscompute/crosscompute-homepage for root.

```bash
sudo -s
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ssh-keygen -t ed25519 -C "crosscompute-homepage-$TIMESTAMP"
```

Test deploy key.

```bash
bash scripts/build.sh
```

Set up packages and services.

```bash
bash scripts/setup-packages.sh
bash scripts/setup-services.sh
```

## Development

```bash
python scripts/serve.py
```
