# ma_scene

Voilà la base de code, elle nécessite openGL et glut, "python-opengl"
sous Arch probablement la même chose ailleurs.

J'ai fait le modèle sous Blender mais ce dernier est peu adapté aux
surfaces implicites donc j'ai passé mon temps à supprimer les sommets
de surfaces explicites, triste histoire…

J'ai choisi le format OBJ car il est très simple.

Utilisation:
    python3 main.py modèles/évier.obj

La souris permet de tourner autour du modèle.
Clic-droit ouvre un menu d'option.

L'exécution sur un fichier .obj génère un fichier "last.pts" dans le
répertoire courant. Donner un fichier .pts en argument évite de
refaire le calcul de la surface.