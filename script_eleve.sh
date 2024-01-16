#!/bin/bash

cd ~/pybot
source .venv/bin/activate
pip install -r requirements.txt
export `cat .env_to_rename`
