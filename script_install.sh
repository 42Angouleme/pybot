#!/bin/bash

sudo apt-get install wget gpg
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -D -o root -g root -m 644 packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
rm -f packages.microsoft.gpg

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y apt-transport-https python3.10 python3.10-venv python3-pip code

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr
