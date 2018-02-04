from sys import argv
from OpenGL.GLUT import *
# je me le permets car les commandes sont préfixées par glut

from obj import litObj
from scene import Scene
from implicit import Implicit

if len(argv)==1:
    argv.append("modèles/cube.obj")
if len(argv)!=2:
    print("Utilisation: ma_scene.py scene.obj")
    exit(1)

points,lignes,faces = litObj(argv[1])

# Traitement des surfaces implicites
####

Ri = 1.0
ki = 10.0
iso = 3
eps = 0.3
step_line = 100
step_cube = 0.5

implicit = Implicit(points, Ri, ki, iso, eps, step_line, step_cube)
print("Points du squelette\n")
print(points)
implicit_points = implicit.compute()

print("Points de la surface implicite\n")
#print(implicit_points)

####


glutInit(1,"")
glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(200,200)
glutInitWindowSize(500,500)
glutCreateWindow(b"Ma scene")

scene = Scene(points,lignes,faces,implicit_points)
scene.associeFonctions()

glutMainLoop()

