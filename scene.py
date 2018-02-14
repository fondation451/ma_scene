from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import sin,cos,pi
from random import random
from time import sleep
from sys import argv, stdout,stderr
from enum import IntEnum

class Mode(IntEnum):
    squelette = 1
    surface   = 2
    animation = 3
    visualise = 4

d2r = 2*pi/360 #degrés (gl et code) vers radians (python.math)

class Scene:
    def __init__(s, animation, lignes, faces, dt):
        s.lat = 30             # latitude
        s.lon = 30             # longitude
        s.xOld, s.yOld = 0, 0  # ancienne position de la souris
        s.animation = animation; s.lignes = lignes; s.faces = faces
        s.time = 0
        s.dt = dt
        s.drawimp = True
        s.mode = Mode.surface
        s.persp = True
        s.light = True
        glutInit(1,"")
        glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE)
        glutInitWindowSize(1000,500)
        s.wMain =  glutCreateWindow(b"Surfaces implicites")
        s.wScene = glutCreateSubWindow(s.wMain,   0, 0, 1000, 500)
        s.wVisu =  glutCreateSubWindow(s.wMain, 500, 0,  500, 500)
        glutHideWindow()
        s.init3d()
        glutSetWindow(s.wScene)
        s.createMenu()
        s.init3d()
        s.associeFonctions()

    def init3d(s):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glClearColor(0,0,0,0)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        s.changePerspective()
        
    def createMenu(s):
        lightMenu = glutCreateMenu(s.menu)
        glutAddMenuEntry("Desactiver".encode("Latin9"), 40)
        glutAddMenuEntry("Activer", 41)
        modeMenu = glutCreateMenu(s.menu)
        s.modeEntries = (
            glutAddMenuEntry("Squelette", 11),
            glutAddMenuEntry("Surface", 12),
            glutAddMenuEntry("Animation", 13),
            glutAddMenuEntry("Visualisation", 14))
        perspMenu = glutCreateMenu(s.menu)
        glutAddMenuEntry("Droite", 30)
        glutAddMenuEntry("Perspective", 31)
        polyMenu = glutCreateMenu(s.menu)
        glutAddMenuEntry("Pleins", 20)
        glutAddMenuEntry("Lignes", 21)
        menuId = glutCreateMenu(s.menu)
        glutAddSubMenu("Mode",modeMenu)
        glutAddSubMenu("Projection",perspMenu)
        glutAddSubMenu("Polygones".encode("Latin9"),polyMenu)
        glutAddSubMenu("Lumiere".encode("Latin9"),lightMenu)
        glutAddMenuEntry("Quitter",1)


    def assocDisplay(s, t):
        print(t, file=stderr)
        s.time = t
        glutDisplayFunc(s.displayScene)
        glutIdleFunc(s.displayScene)


    def associeFonctions(s):
        for i in range(0, len(s.animation)):
            glutTimerFunc(i * s.dt, s.assocDisplay, i)
        glutDisplayFunc(s.displayScene)
        glutReshapeFunc(s.reshape)
        glutMouseFunc(s.mouse)
        glutMotionFunc(s.move)

        glutSetWindow(s.wMain)
        glutReshapeFunc(s.wreshape)
        glutDisplayFunc(lambda:None)
        #glutIdleFunc(s.idle)

        glutSetWindow(s.wVisu)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        glutKeyboardFunc(s.kbd)
        glClearColor(0,0,0,0)#1,1,1,0)
        glutDisplayFunc(s.displayScene)
        glutReshapeFunc(s.reshape)

        glutSetWindow(s.wScene)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        glutKeyboardFunc(s.kbd)
        glutDisplayFunc(s.displayScene)
        glutReshapeFunc(s.reshape)
        glutMouseFunc(s.mouse)
        glutMotionFunc(s.move)

    def main(s): glutMainLoop()
        
    def displayVisu(s):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glutSwapBuffers()#glFlush()
        
    def displayScene(s):
        "Tout l'affichage se fait ici"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        points, imppoints = s.animation[s.time]

        # on se recule (sinon on a le nez dans le lavabo)
        glTranslate(0,0,-8)
        # on tourne selon l'axe vertical, facile
        glRotate(s.lon,0,1.0,0)
        # on tourne selon un compromis entre l'axe x et l'axe z pour lever la caméra
        glRotate(s.lat,cos(d2r*s.lon),0,sin(d2r*s.lon)) #

        if s.mode==Mode.squelette:
            glColor3f(1,0,0)
            for i in s.faces:
                glBegin(GL_POLYGON)
                for j in i:
                    glVertex3f(*points[j[0]-1])
                glEnd()

            glColor3f(.8,.8,0)
            for a,b in s.lignes:
                glBegin(GL_LINES)
                glVertex3f(*points[a-1])
                glVertex3f(*points[1])
                glEnd()
        if s.mode>Mode.squelette:
            glColor3f(1,1,1)
            for l in imppoints:
                #glColor3f(random(),random(),random())
                glBegin(GL_POLYGON)
                for p in l:
                    glNormal3f(*p[1])
                    glVertex3f(*p[0])
                glEnd()
        glutSwapBuffers()#glFlush()


    def menu(s,p):
        if p==1: exit()
        elif 10<p<15:
            oldMode = p
            s.mode = p-10
            if oldMode==Mode.visualise or s.mode==Mode.visualise: s.wreshape(*s.size)
        elif p in (20,21):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL if p==20 else GL_LINE)
        elif p in (30,31):
            s.persp = p-30
            s.changePerspective()
        elif p in (40,41):
            glEnable(GL_LIGHTING) if p==41 else glDisable(GL_LIGHTING)
        return 0
        
    def wreshape(s,w,h):
        s.size = w,h
        if s.mode==Mode.visualise:
            glutSetWindow(s.wScene)
            glutReshapeWindow(w//2,h)
            glutSetWindow(s.wVisu)
            glutPositionWindow(w//2,0)
            glutReshapeWindow(w//2,h)
            glutShowWindow()
        else:
            glutSetWindow(s.wScene)
            glutReshapeWindow(w,h)
            glutSetWindow(s.wVisu)
            glutHideWindow()

    def reshape(s,w,h):
        "Fait en sorte que la scene soit carrée et centree"
        if w<h: glViewport(0,(h-w)//2,w,w)
        else:   glViewport((w-h)//2,0,h,h)

    def kbd(s,k,x,y):
        if k==b'q': exit()
        elif k==b'v':
            s.mode = Mode.surface if s.mode==Mode.visualise else Mode.visualise
            s.wreshape(*s.size)

    def mouse(s,b,e,x,y):
        if b==GLUT_LEFT_BUTTON and e==GLUT_DOWN:
            s.xOld=x
            s.yOld=y

    def move(s,x,y):
        s.xOld, s.lon = x, (s.lon+x-s.xOld)%360
        s.yOld, s.lat = y, (s.lat+y-s.yOld)%360
        glutPostRedisplay()

    def idle(s,*p):
        s.lon += 1
        glutPostRedisplay()

    def changePerspective(s):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if s.persp: gluPerspective(50,1.0,0.1,40.0)
        else:       glOrtho(-3,3,-3,3,-10,10)
        glMatrixMode(GL_MODELVIEW)


