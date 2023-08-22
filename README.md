# PROJET ROBOT PYTHON

[![Python Check](https://github.com/42Angouleme/robot-python/actions/workflows/python-app.yml/badge.svg)](https://github.com/42Angouleme/robot-python/actions/workflows/python-app.yml)

* Une présentation complète du projet ici :
```
documentation/hackathon.pdf
```

## Planning

### HACKATHON
* Starting date : 16 Août 2023 - 9h
* 1st Meeting : 16 Août 2023 - 9h
* End date : 17 Août 2023 - 18h
* 2nd Meeting : 17 Août 2023 - 16h

## Objectifs
* Une présentation de chaque module se trouve dans le pdf :
    * Module microphone
    * Module speaker
    * Module camera
    * Module matrix screen
    * Module web app
    * Module openia
    * Un autre module proposé ?

## Setup environnement dev python
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Ajouter un package python et tout ajouter au fichier requirements.txt
```
python3 -m pip install <package_name>
python3 -m pip freeze >> requirements.txt
```

## Lancer le programme principal

```
python3 main.py
```
ou
```
chmod +x main.py
./main.py
```

## Démo interractives avec JupyterLab

### Setup

Setup à ne faire qu'une fois. Placez-vous à la racine du projet avec l'environnement virtuel activé et lancez la commande suivante.

``` sh
ipython profile create && echo "c.InteractiveShellApp.exec_lines = ['import sys; sys.path.append(\"$(pwd)\")']" >> ~/.ipython/profile_default/ipython_config.py
```
> Celà permet au notebook de trouver les modules locaux à notre package

La dernière ligne du fichier `~/.ipython/profile_default/ipython_config.py` devraient maintenant contenir:

``` python
c.InteractiveShellApp.exec_lines = ['import sys; sys.path.append("<chemin_vers_robot-python>")']
```

### Lancer les démo

``` sh
jupyter lab notebooks/sommaire.ipynb
```

> Les notebooks [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/index.html) combinent descriptions Markdown et sections de code interractif.
