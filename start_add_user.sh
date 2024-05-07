#!/bin/bash

cd /home/eliot/Documents/"Projet Robot"/pybot
python3 -m venv --system-site-packages venv
source venv/bin/activate
python3 -m pip install -Ir requirements.txt
python3 add_user_to_database.py
