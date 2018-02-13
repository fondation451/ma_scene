from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import sin,cos,pi
from random import random
from time import sleep

d2r = 2*pi/360 #degrés (gl et code) vers radians (python.math)

class Scene:
    def __init__(s, points, lignes, faces, imppoints):
        s.lat = 30             # latitude
        s.lon = 30             # longitude
        s.xOld, s.yOld = 0, 0  # ancienne position de la souris
        s.points = points; s.lignes = lignes; s.faces = faces
        s.imppoints = imppoints
        s.drawimp = True
        s.persp = True
        s.light = True
        s.createMenu()
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
        glutAddMenuEntry("Squelette", 10)
        glutAddMenuEntry("Surface", 11)
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

    def associeFonctions(s):
        glutDisplayFunc(s.display)
        glutReshapeFunc(s.reshape)
        glutMouseFunc(s.mouse)
        glutMotionFunc(s.move)
        #glutIdleFunc(s.idle)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        glutKeyboardFunc(s.kbd)

    def display(s):
        "Tout l'affichage se fait ici"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # on se recule (sinon on a le nez dans le lavabo)
        glTranslate(0,0,-8)
        # on tourne selon l'axe vertical, facile
        glRotate(s.lon,0,1.0,0)
        # on tourne selon un compromis entre l'axe x et l'axe z pour lever la caméra
        glRotate(s.lat,cos(d2r*s.lon),0,sin(d2r*s.lon)) #

        glColor3f(1,0,0)
        for i in s.faces:
            glBegin(GL_POLYGON)
            for j in i:
                glVertex3f(*s.points[j[0]-1])
            glEnd()

        glColor3f(.8,.8,0)
        for a,b in s.lignes:
            glBegin(GL_LINES)
            glVertex3f(*s.points[a-1])
            glVertex3f(*s.points[b-1])
            glEnd()

        if s.drawimp:
            glColor3f(1,1,1)
            for l in s.imppoints:
                #glColor3f(random(),random(),random())
                glBegin(GL_POLYGON)
                for p in l:
                    glNormal3f(*p[1])
                    glVertex3f(*p[0])
                glEnd()

        glFlush()

    def menu(s,p):
        if p==1: exit()
        elif p in (10,11):
            s.drawimp = p-10
        elif p in (20,21):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL if p==20 else GL_LINE)
        elif p in (30,31):
            s.persp = p-30
            s.changePerspective()
        elif p in (40,41):
            glEnable(GL_LIGHTING) if p==41 else glDisable(GL_LIGHTING)
        return 0

    def reshape(s,w,h):
        "Fait en sorte que la scene soit carrée et centree"
        if w<h: glViewport(0,(h-w)//2,w,w)
        else:   glViewport((w-h)//2,0,h,h)

    def kbd(s,k,x,y):
        if k==b'q': exit()
        else: return

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
#        sleep(0.)
        glutPostRedisplay()

    def changePerspective(s):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if s.persp: gluPerspective(50,1.0,0.1,40.0)
        else:       glOrtho(-3,3,-3,3,-10,10)
        glMatrixMode(GL_MODELVIEW)


