#!/bin/bash

apt update && apt upgrade python3
apt install -y python3.10-venv python3-pip code

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr
