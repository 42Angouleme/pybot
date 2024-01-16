#!/bin/bash

sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install --user -y flathub com.visualstudio.code
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y apt-transport-https python3.10 python3.10-venv python3-pip

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr
