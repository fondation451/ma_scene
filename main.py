from sys import argv
from OpenGL.GLUT import *
# je me le permets car les commandes sont préfixées par glut

from obj import litObj
from scene import Scene

if len(argv)!=2:
    print("Utilisation: ma_scene.py scene.obj")
    exit(1)

points,lignes,faces = litObj(argv[1])

glutInit(1,"")
glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(200,200)
glutInitWindowSize(500,500)
glutCreateWindow(b"Ma scene")

scene = Scene(points,lignes,faces)
scene.associeFonctions()

glutMainLoop()

