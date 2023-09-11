# Interactions

Interaction entre modules.

## Track cards [module webapp & camera]

Sur l'image donnée, cherche des rectangles noir, détour et ajuste la perspective. Tourne les images détourées de manière à ce que le coin qui a une tâche noir soit en haut à droite. Récupère les utilisateurs en BD et filtre ceux dont l'image a une forte similarité avec les images détourées.

### Application démo

``` sh
# cd à la racine du projet robot-python
python3 -m interactions.track_user_cards.demo.app
```

> Cela lance:
>
> - le serveur qui se connecte à une base de donnée de test située à `track_user_cards/demo`
> - l'application de reconnaissance de cartes dans un thread

Maintenant, sur un téléphone par exemple, ouvrez une des images situé dans `track_user_cards/demo/img_to_show` et montrez-le à votre caméra.

> Attention au reflets qui perturbent la détection sur téléphone, idéalement il faut une surface papier

Votre image devrait s'afficher avec une bordure colorée et le nom d'utilisateur s'affiche à côté.
