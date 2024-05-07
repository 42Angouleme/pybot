#!/bin/bash

cd /home/eliot/Documents/"Projet Robot"/pybot
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 add_user_to_database.py
