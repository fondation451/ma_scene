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

if argv[1].endswith(".pts"):
    with open(argv[1],"rb") as f:
        points,lines,faces = load(f)
        implicit_points = load(f)
else:
    with popen("pypy3 calc.py "+argv[1]+" | tee last.pts") as f:
        points,lines,faces = load(f.buffer)
        implicit_points = load(f.buffer)

glutInit(1,"")
glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH)
glutInitWindowPosition(200,200)
glutInitWindowSize(500,500)
glutCreateWindow(b"Ma scene")

scene = Scene(points,lines,faces,implicit_points)
scene.associeFonctions()

glutMainLoop()

