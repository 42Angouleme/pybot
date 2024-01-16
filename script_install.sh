#!/bin/bash

cd

git clone https://github.com/42Angouleme/pybot.git
cd pybot

su - 

apt install python3.10-venv python3-pip code

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr

exit

/usr/bin/python3.10 -m venv .venv
