# CrossCompute Homepage

## Installation

Become root and make an SSH key.

```bash
sudo -s
ssh-keygen -t ed25519 -C "crosscompute-homepage-$(date +%Y%m%d-%H%M%S)"
```

[Add the SSH key as a deploy key to this repository](https://github.com/crosscompute/crosscompute-homepage/settings/keys).

Set up packages and services.

```bash
sudo -s
bash scripts/setup-packages.sh
bash scripts/setup-services.sh
```

Test the deploy key.

```bash
sudo -s
bash scripts/build.sh
systemctl start crosscompute-homepage
```

## Development

```bash
python scripts/serve.py datasets/configuration.yml
```
