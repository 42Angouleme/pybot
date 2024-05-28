#!/bin/bash

cd /home/pybot/pybot
source venv/bin/activate
python3 -m pip install -Ir requirements.txt
python3 main.py
