# Pybot

[![Python Check](https://github.com/42Angouleme/robot-python/actions/workflows/python-app.yml/badge.svg)](https://github.com/42Angouleme/robot-python/actions/workflows/python-app.yml)

> Un projet maintenu par les étudiants de l'école 42 pour aider des collégiens à découvrir la programmation.

Une question ?, voir la [Documentation](https://42angouleme.github.io/).


## Configurer l'environnement python et installer les dépendances

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

```sh
ipython profile create && echo "c.InteractiveShellApp.exec_lines = ['import sys; sys.path.append(\"$(pwd)\")']" >> ~/.ipython/profile_default/ipython_config.py
```

> Celà permet au notebook de trouver les modules locaux à notre package

La dernière ligne du fichier `~/.ipython/profile_default/ipython_config.py` devraient maintenant contenir:

```python
c.InteractiveShellApp.exec_lines = ['import sys; sys.path.append("<chemin_vers_robot-python>")']
```

### Lancer les démo

```sh
jupyter lab notebooks/sommaire.ipynb
```

> Les notebooks [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/index.html) combinent descriptions Markdown et sections de code interractif.
