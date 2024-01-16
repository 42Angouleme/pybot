#!/bin/bash

rm -rf /etc/apt/sources.list.d/additional-repositories.list.d/vscode.list
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update && install -y code
