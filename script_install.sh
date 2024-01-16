#!/bin/bash

su prof

apt install python3.10-venv python3-pip code

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr

exit

/usr/bin/python3.10 -m venv .venv
