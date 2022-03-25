#!/bin/bash
TIMESTAMP=$(date +%Y%m%d-%H%M)
FOLDER=/srv/crosscompute-homepage-$TIMESTAMP

cd ~/Projects/crosscompute-homepage
git checkout master
git pull

source \
    ~/.virtualenvs/crosscompute-homepage/bin/activate
python \
    scripts/build.py \
    datasets/configuration.yml \
    $FOLDER

ln -snf $FOLDER /srv/crosscompute-homepage
