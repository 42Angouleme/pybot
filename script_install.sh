#!/bin/bash

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr
