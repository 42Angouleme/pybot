#!/bin/bash

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr
rm -rf .venv
/usr/bin/python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo "export `cat .env_to_rename | tr '\n' ' '` PATH=$HOME/pybot/.venv/bin:$PATH" >> $HOME/.bashrc
