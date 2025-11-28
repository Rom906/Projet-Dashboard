# Projet-Dashboard

# Manuel d'utilisation de la dashboard :

## Prérequis :

Les fichiers python page_donnees_v2.py, page_graphiques_v2.py et main_v2.py ainsi qu'un fichier de données au format csv.
Il faut au préalable installer la bibliothèque streamlit à l'aide de la commande 'pip install streamlit' dans le terminal.


## Lancement du dashboard :

La dashboard se lance en exécutant le script main_v2 via la commande streamlit run main_v2.py.

On atterit ensuite sur le site web de la dashboard hébergé en local sur notre propre ordinateur.
Nous nous trouvons d'abord sur la page de données et il faut glisser et déposer un fichier csv qui contiendra les données qui seront utilisées pour la dashboard. Les données doivent être rangées en colonnes pour être traduites correctement pour le code.

Les données seront ensuite visible sur la page dans un tableau si l'import a été fait avec succès.


## Prise en main et début de la création de dashboard :

Nous serons par défaut sur la page des données de notre dashboard mais le menu à gauche permet de changer de page facilement. Pour cela, il faut utiliser le menu déroulant où il y a écrit 'Page de données' et cliquer dessus puis cliquer sur 'Page Graphiques' pour aller sur l'autre page de la dashboard qui est celle où on affichera tous les graphiques et données marquantes. 

C'est d'ailleurs avec cette partie du site que l'on peut intéragir. En effet, cette page est par défaut vierge car c'est à l'utilisateur de l'implémenter. Pour cela, il a accès à différentes fonctionnalités dans le menu à gauche de l'écran.


## Fonctionnalités de l'outil de création :

Pour implémenter des graphiques, des zones de textes ou autres visuels, il faut créer des zones dédiées et pour créer ces zones, il faut leur allouer des lignes.

Pour commencer à implémenter sa dashboard avec des graphiques ou autres visuels, il faut donc ajouter une ligne à l'aide du bouton 'Créer une nouvelle ligne'. Il faut impérativement lui mettre un titre que l'on pourra afficher ou non en cochant la case 'Afficher le titre' juste en dessous du bouton. Ce dernier permet de différencier les lignes entre elles et donc doit être différent d'une ligne à l'autre?????
Il n'y a pas de limite au nombre de lignes que l'on peut mettre dans la dashboard.

Ensuite, nous pouvons rajouter des zones de graphiques dans les lignes que l'on appelle des 'areas'. Pour cela, il faut aller dans la partie du menu à gauche de l'écran qui s'appelle 'Ajouter une zone de graphique'.

