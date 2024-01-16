#!/bin/bash

sudo apt-get install -y wget gpg

curl -fSsL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor | sudo tee /usr/share/keyrings/vscode.gpg > /dev/null
echo deb [arch=amd64 signed-by=/usr/share/keyrings/vscode.gpg] https://packages.microsoft.com/repos/vscode stable main | sudo tee /etc/apt/sources.list.d/vscode.list

sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y apt-transport-https python3.10 python3.10-venv python3-pip code

code --install-extension ms-python.python
code --install-extension MS-CEINTL.vscode-language-pack-fr
