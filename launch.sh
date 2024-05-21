#!/bin/bash

cd /home/pybot/pybot
python3 -m venv --system-site-packages venv
source venv/bin/activate
python3 -m pip install -Ir requirements.txt
python3 main.py