# projet_ROBVIS
### Projet UV ROBVIS : amélioration de jeu sur le robot ABB YUMI

L'objectif du projet est de développer de nouveaux programmes et stratégies de jeu du morpion avec le robot ABB YUMI.
Ce robot était déjà programmé pour jouer à une partie de morpion classique avec un humain ainsi que ranger les pièces une fois la partie terminée.

Nous avons décidé de programmer le robot pour jouer à une partie de morpions à 3 pièces seulement. C'est-à-dire, que les 3 premiers tours du joueur humain et du robot sont réalisés normalement, puis pour les tours suivant, les joueurs déplacent la plus ancienne pièce qu'ils ont posé au lieu d'en prendre une quatrième. Cela complexifie vraiment le jeu et permet à l'humain d'avoir une chance contre l'ordinateur.


### Règle du jeu :
Le but du jeu est d'aligner 3 pièces dans un plateau de 3 par 3. L'adversaire possède lui aussi 3 pièce. Le premier qui réussi à aligner ses 3 pièces gagne et l'autre perd. Le jeu se joue à tour de rôle et si plus de 50 coups sont joués, la partie est déclarée nulle. 
Le joueur humain commence la parti en posant de l'emplacement 15 sur le plateau sa première pièce(important pour le rangement). Après avoir posé ses 3 premières pièces des emplacements 15, 16 et 17. L'ordinateur indique quelle pièce doit être enlevée pour être replacée (obligatoirement à un autre emplacement libre). 
La partie continue jusqu'à ce qu'un joueur soit déclaré vainqueur ou que la partie soir déclarée nulle.
Bonne chance!


### Instruction d'installation : 

 - Utiliser l'ordinateur prévu à l'emplacement du robot ABB YUMI
 - Lancer *RobotStudio 2021*
 - Ajouter le controlleur le plus récent
 - Charger la backup datant du 24 Mars 2025
 - Aller chercher dans le dossier *Projet LauAntBen*, le fichier *MainModule.mod*, l'ouvrir , et copier l'intégralité du contenu dans le *MainModule.mod* du bras droit du robot (Une copie de la version de base du *MainModule.mod* existe déjà dans le même dossier dans l'idée de remettre le programme de base)
 - Dans le dossier *LauAntBen* ouvrir le code python *Version_morpion_3_pieces.py* et le copier
 - Dans le dossier tictactoe ouvir le code Python *V1_server_tictactoe.py* et remplacer son contenue par le code précédemment copié
 - Dans le bureau, lancer le programme *LancementJeuTicTacToe _ Copie.BAT*
 - Dans *robotstudio*, Set les pointeurs puis appuyer sur start
 - La partie va démarrer après un check (tapoter le bout du robot) avec le robot 

### Liste des fichiers 

- *V1_server_tictactoe.py* : le code python original à utiliser avec le robot pour jouer au morpion simple
- *Version_morpion_3_pieces.py* : le code modifié pour jouer au morpion à 3 pièces
- *version_py_jeu_original.py* : Un code python qui reprend la version pour robot mais l'adapte pour pouvoir réaliser une partie de morpion directement sur un terminal python avec l'IA du robot
- *version_py_jeu_3_pieces_v3.py* : Le code python pour jouer sur le terminal adapté au jeu de morpion à trois pièces

### Nos modifications
-Dans le code Python qui permet de choisir le prochain coup (voir les commentaires dans le fichier *version_py_jeu_3_pieces_v3.py* 
-Dans le code qui permet de lancer le robot *MainModule.mod* dans la fonction Game(). Nous avons modifié la structure du jeu pour que les trois premier coups viennent de la reserve de pions et que les coups suivants soit pris depuis le plateau, en récuperant la bonne pièce. Les modules de visons et de mouvements restent inchangés  
 
