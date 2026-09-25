#!/bin/sh
set -eu
cd /home/ubuntu/healthcare-claim-denial-agent
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
sudo -n install -m 644 deploy/claim-resolve-api.service /etc/systemd/system/claim-resolve-api.service
sudo -n systemctl daemon-reload
sudo -n systemctl enable --now claim-resolve-api
