from sys import argv
from os import popen
from OpenGL.GLUT import *
from pickle import load
# je me le permets car les commandes sont préfixées par glut

from scene import Scene

if len(argv)==1:
    argv.append("modèles/cube.obj")
if len(argv)!=2:
    print("Utilisation: ma_scene.py scene.obj")
    exit(1)

with popen("pypy3 calc.py "+argv[1]) as f:
    points,lines,faces = load(f.buffer)
    implicit_points = load(f.buffer)
#exit()
print(points)
print(lines)
print(len(implicit_points))

glutInit(1,"")
glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(200,200)
glutInitWindowSize(500,500)
glutCreateWindow(b"Ma scene")

scene = Scene(points,lines,faces,implicit_points)
scene.associeFonctions()

glutMainLoop()

