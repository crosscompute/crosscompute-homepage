# CrossCompute Homepage

## Installation

Become root and make an SSH key.

```bash
sudo -s
ssh-keygen -t ed25519 -C "crosscompute-homepage-$(date +%Y%m%d-%H%M%S)"
```

[Add the SSH key as a deploy key to this repository](https://github.com/crosscompute/crosscompute-homepage/settings/keys).

Set up the deploy key ssh configuration.

```bash
vim ~/.ssh/config
    Host gh-homepage
    Hostname github.com
    IdentityFile ~/.ssh/crosscompute-homepage
    IdentitiesOnly yes
```

Clone the repository using the deploy key.

```bash
git clone git@gh-homepage:crosscompute/crosscompute-homepage
```

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
systemctl restart crosscompute-homepage
```

## Development

```bash
python scripts/serve.py datasets/configuration.yml
```
