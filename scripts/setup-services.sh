#!/bin/bash
sudo cp services/* /etc/systemd/system
sudo systemctl daemon-reload
# sudo systemctl enable crosscompute-homepage.service
# sudo systemctl enable crosscompute-homepage.timer
sudo systemctl start crosscompute-homepage.service
sudo systemctl start crosscompute-homepage.timer
