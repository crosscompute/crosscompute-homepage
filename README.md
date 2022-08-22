# CrossCompute Homepage

## Installation

1. Become root and make an SSH key.

```bash
sudo -s
ssh-keygen -t ed25519 -C "crosscompute-homepage-$(date +%Y%m%d-%H%M%S)"
```

2. [Add the SSH key as a deploy key to this repository](https://github.com/crosscompute/crosscompute-homepage/settings/keys).
3. Test the deploy key.

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
