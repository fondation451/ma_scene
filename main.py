from sys import argv
from OpenGL.GLUT import *
# je me le permets car les commandes sont préfixées par glut

from obj import litObj
from scene import Scene
from implicit import Implicit

if len(argv)!=2:
    print("Utilisation: ma_scene.py scene.obj")
    exit(1)

points,lignes,faces = litObj(argv[1])


# Traitement des surfaces implicites
####

Ri = 100.0
ki = 10.0
iso = 10
eps = 0.01
step_line = 0.1
step_cube = 0.1

implicit = Implicit(points, Ri, ki, iso, eps, step_line, step_cube)
print("Points du squelettes\n")
print(points)
points = implicit.compute()

print("Points de la surface implicite\n")
print(points)

exit(0)

####


glutInit(1,"")
glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(200,200)
glutInitWindowSize(500,500)
glutCreateWindow(b"Ma scene")

scene = Scene(points,lignes,faces)
scene.associeFonctions()

glutMainLoop()

