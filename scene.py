from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import sin,cos,pi
from random import random
    
d2r = 2*pi/360 #degrés (gl et code) vers radians (python.math)

class Scene:
    def __init__(s, points, lignes, faces, imppoints):
        s.lat = 30             # latitude
        s.lon = 30             # longitude
        s.xOld, s.yOld = 0, 0  # ancienne position de la souris
        s.points = points; s.lignes = lignes; s.faces = faces
        s.imppoints = imppoints
        s.drawimp = True
        glEnable(GL_DEPTH_TEST)
        # glEnable(GL_LIGHTING) j'ai voulu mettre de la lumière pour améliorer le contraste
        # glEnable(GL_LIGHT0)   mais il faut définir les normales pour que ça marche
        # glLightfv(GL_LIGHT0, GL_DIFFUSE, (255,0,0))
        # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (255,255,255))
        glClearColor(0,0,0,0)
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)#GL_LINE pour voir en fil de fer
        s.changePerspective()

    def associeFonctions(s):
        glutDisplayFunc(s.display)
        glutReshapeFunc(s.reshape)
        glutMouseFunc(s.mouse)
        glutMotionFunc(s.move)
        #glutIdleFunc(idle) animation par ici
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

        for i in s.faces:
            glBegin(GL_POLYGON)
            for j in i:
                glColor3f(random(),random(),random()) # couleur aléa-beurk
                glVertex3f(*s.points[j[0]-1])
            glEnd()
            
        for a,b in s.lignes:
            glBegin(GL_LINES)
            glColor3f(random(),random(),random())
            glVertex3f(*s.points[a-1])
            glVertex3f(*s.points[b-1])
            glEnd()

        if s.drawimp:
            glColor3f(1,1,1)
            for l in s.imppoints:
                glBegin(GL_POLYGON)
                for p in l:
                    glVertex3f(*p)
                glEnd()
            
        glFlush()

    def reshape(s,w,h):
        "Fait en sorte que la scène soit carrée et centrée"
        if w<h: glViewport(0,(h-w)//2,w,w)
        else:   glViewport((w-h)//2,0,h,h)

    def kbd(s,k,x,y):
        k = k.translate(bytes.maketrans(b"zqsdx",b"rtsnq")) # adaptation à mon clavier
        if k==b'q': exit()
        elif k==b'r': s.lat+=1
        elif k==b's': s.lat-=1
        elif k==b't': s.lon+=1
        elif k==b'n': s.lon-=1
        elif k==b'b': s.drawimp = not s.drawimp
        else: return
        s.lat%=360; s.lon%=360
        glutPostRedisplay()

    def mouse(s,b,e,x,y):
        if b==GLUT_LEFT_BUTTON and e==GLUT_DOWN:
            s.xOld=x
            s.yOld=y

    def move(s,x,y):
        s.xOld, s.lon = x, (s.lon+x-s.xOld)%360
        s.yOld, s.lat = y, (s.lat+y-s.yOld)%360
        glutPostRedisplay()

    def changePerspective(s):
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(50,1.0,0.1,40.0);
        glMatrixMode(GL_MODELVIEW);


