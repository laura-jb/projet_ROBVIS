# projet_ROBVIS
### Projet UV ROBVIS : amélioration de jeu sur le robot ABB YUMI

L'objectif du projet est de développer de nouveaux programmes et stratégies de jeu du morpion avec le robot ABB YUMI.
Ce robot était déjà programmé pour jouer à une partie de morpion classique avec un humain ainsi que ranger les pièces une fois la partie terminée.

Nous avons décidé de programmer le robot pour jouer à une partie de morpions à 3 pièces seulement. C'est-à-dire, que les 3 premiers tours du joueur humain et du robot sont réalisés normalement, puis pour les tours suivant, les joueurs déplacent la plus ancienne pièce qu'ils ont posé au lieu d'en prendre une quatrième.

### Instruction d'installation : 

 - Utiliser l'ordinateur prévu à l'emplacement du robot ABB YUMI
 - Lancer RobotStudio 2021
 - Ajouter le controlleur le plus récent
 - Charger la backup datant du 24 Mars 2025
 - Aller chercher dans le dossier Projet LauAntBen, le fichier MainModule.mod, l'ouvrir , et copier l'intégralité du contenue dans le MainModule.mod du bras droit du robot (Une copie de la version de base du MainModule.mod existe déjà dans le même dossier dans l'idée de remettre le programme de base)
 - Dans le dossier LauAntBen ouvrir le code python Version_morpion_3_pieces.py et copier le
 - Dans le dossier tictactoe ouvir le code Python V1_server_tictactoe.py et remplacer son contenue par le code précédemment copié
 - Dans le bureau, lancer le programme LancementJeuTicTacToe _ Copie.BAT
 - Dans robotstudio, Set les pointeurs puis appuyer sur start
 - La partie va démarrer après un check avec le robot 

### Liste des fichiers 


