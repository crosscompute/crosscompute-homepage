#!/bin/bash
sudo cp services/* /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable crosscompute-homepage
sudo systemctl start crosscompute-homepage
