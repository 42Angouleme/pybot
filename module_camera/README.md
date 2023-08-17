# Module Camera


## Objective:

Détecter et reconnaitre les dessins des collégiens.

## Comment procéder

- Contraintes
- Connection de la caméra
- Faire des cartes testes
- Détection des dessins
- Comparaison
- Remplissage de la base de données
- Connection avec la base de données

##  Les contraintes matériel

### Impératif

- La caméra doit être fixe.
- Avoir un éclairage constant.
- Le modèle de carte doit respecter un format standard.
- 1 dessin ne peut être changé, on ne peut pas rajouter de la couleur.
- 1 dessin = 1 personne (les couleurs ne se différencient pas suffisement avec notre algorithme).
- La carte sera placé dans un sens particulier.

### Suggestions

- La caméra doit être en plongée.
- Utiliser des leds pour avoir un éclairge constant
- Utiliser un support bordé pour mettre la carte à une place fixe.
- Les cartes peuvent avoir le format des cartes de visite.
- Possibilité de rajouter une fontion pour retourner la carte à 360 degré

## Connection de la caméra 

Pour connecter la caméra à une raspberry Pi suivre ce tutoriel:
https://projects.raspberrypi.org/fr-FR/projects/getting-started-with-picamera/1

## Détection des dessins

- Utilisation du module OpenCV.

## Comparaisson

- Utilistation de l'algorithme Structural Similarity Index (SSIM)
- Pour l'utilisation du module scikit-image .

## Remplissage de la base de données

Work in progress...

faire une vérification si le dessin n'est pas déjà présent dans la base de donnée.


## Connection avec la base de données

Work in progress... Structural Similari