Optimisé pour modèles/cubelignes.obj.

Pb: quelques polygones ont des sommets qui divergent pour certaines
valeur de Ri avec cube.


Nécessite OpenGL et Glut, "python-opengl" et éventuellement pypy3 pour
la vitesse.

La souris permet de tourner autour du modèle.
Clic-droit ouvre un menu d'option.

L'exécution sur un fichier .obj génère un fichier "last.pts" dans le
répertoire courant. Donner un fichier .pts en argument évite de
refaire le calcul de la surface.

Utilisation:
    python3 main.py modèles/évier.obj
