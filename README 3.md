# Rôle de chaque fichier dans mon dossier src/

Structure du dossier src

    main.py : C'est le chef d'orchestre. Il contient la boucle principale (mainloop), gère les événements Pygame (clics de souris, touches clavier) et initialise les objets Game et Screen.

    board.py : Le cerveau logique. Il contient la classe Board, gère la matrice 8x8, le placement initial des pièces et, surtout, la logique de calcul des mouvements valides (vérifier si une case est occupée, gérer les échecs au roi).

    game.py : Le moteur de rendu et les règles. Il fait le lien entre la logique du plateau et l'affichage. Il gère les tours des joueurs, dessine l'échiquier et les pièces (via show_pieces), et surligne les cases pour les mouvements possibles.

    piece.py : Le modèle de données. Il définit la classe parente Piece et les sous-classes pour chaque type (Pion, Cavalier, Fou, Tour, Dame, Roi). C'est ici qu'on définit la valeur de chaque pièce et le chemin vers sa texture.

    square.py : La brique de base. Une classe simple qui définit une case (coordonnées x, y) et vérifie si elle contient une pièce.

    move.py : L'objet mouvement. Il stocke les coordonnées de départ et d'arrivée d'un coup, ce qui est crucial pour "jouer" et "annuler" des coups pendant que l'IA réfléchit.

    dragger.py : La gestion visuelle du glisser-déposer. Il permet de suivre la souris et de faire "flotter" la pièce sélectionnée au-dessus du plateau pendant que tu la déplaces.

Esthétique et Configuration (Pour l'experience utilisateur)

    const.py : C'est le fichier des paramètres globaux immuables. Il définit la taille de la fenêtre, le nombre de lignes/colonnes (8x8), et surtout la taille des cases (SQSIZE). C'est ici qu'on centralise tout pour éviter les "nombres magiques" dans le code.

    config.py : Contrairement aux constantes, ce fichier gère les préférences utilisateur. Il charge les thèmes, les sons, et fait le lien entre les fichiers de ressources (images/sons) et le reste de l'application.

    color.py : Un petit fichier utilitaire qui définit les objets de couleur (souvent des tuples RGB). Il permet de donner des noms clairs comme LIGHT_GREEN ou DARK_BROWN au lieu de manipuler des chiffres complexes.

    theme.py : Ce fichier définit la classe Theme. Il regroupe les paires de couleurs (case claire / case foncée) et les couleurs de surbrillance (mouvements possibles, dernier coup joué). C'est ce qui te permet de changer le look du jeu (ex: passer d'un thème "Bois" à un thème "Bleu").

    sound.py : Il gère les effets sonores. Il contient la logique pour charger et jouer les fichiers audio lors d'une capture, d'un échec au roi ou d'un déplacement standard.

    NB : Reset complet : La touche R réinitialise tout sans quitter, ce qui est une exigence de ton TP.