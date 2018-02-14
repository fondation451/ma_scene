from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import sin,cos,pi
from random import random
from enum import IntEnum

class Mode(IntEnum):
    squelette = 1
    surface   = 2
    animation = 3
    visualise = 4

d2r = 2*pi/360 #degrés (gl et code) vers radians (python.math)

class Scene:
    def __init__(s, points, lignes, faces, imppoints, imp):
        s.lat = 30             # latitude
        s.lon = 30             # longitude
        s.plat = 0             # latitude
        s.plon = 0             # longitude
        s.phau = 0             # hauteur
        s.xOld, s.yOld = 0, 0  # ancienne position de la souris
        s.points = points; s.lignes = lignes; s.faces = faces
        s.imp = imp
        s.imppoints = imppoints
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
        glEnable(GL_TEXTURE_2D);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glutSetWindow(s.wScene)
        s.createMenu()
        s.init3d()
        s.associeFonctions()

    def calcText(s):
        def couleur(v):
            v = (v-mn)/(mx-mn)
            v = min(v,1)
            v = v**0.4
#            if v%0.05>0.045:
#                return 255,255,255
            return 0,0,int(255*v)
            if v<0.5:
                return 0,0,int(256*v*2)
            else:
                return 0,int(255*v*2-256),int(511-256*v*2)

        if s.mode!=Mode.visualise: return
        z = 64
        sl = s.imp.slice(z,s.plon,s.plat,s.phau)
        mn = 0#min(min(c) for c in sl)
        mx = 10#max(max(c) for c in sl)
        data = bytearray(z*z*3)
        for x,c in enumerate(sl):
            for y,v in enumerate(c):
                data[3*(z*x+y):3*(z*x+y)+3] = couleur(v)
        glTexImage2D(GL_TEXTURE_2D, 0,GL_RGB, z, z, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
        
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

    def associeFonctions(s):
        glutSetWindow(s.wMain)
        glutReshapeFunc(s.wreshape)
        glutDisplayFunc(lambda:None)
        #glutIdleFunc(s.idle)

        glutSetWindow(s.wVisu)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
        glutKeyboardFunc(s.kbd)
        glClearColor(0,0,0,0)#1,1,1,0)
        glutDisplayFunc(s.displayVisu)
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
        s.calcText()
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_POLYGON)
        glTexCoord2d(0,0)
        glVertex2f(-0.5,-0.5)
        glTexCoord2d(0,1)
        glVertex2f(-0.5, 0.5)
        glTexCoord2d(1,1)
        glVertex2f( 0.5, 0.5)
        glTexCoord2d(1,0)
        glVertex2f( 0.5,-0.5)
        glEnd()
        glutSwapBuffers()
        
    def poly(s):
        glDisable(GL_LIGHTING)
        glBegin(GL_POLYGON)
        glColor3f(0.9,0.9,0.5)
        glNormal3f( 0, 1, 0)
        glVertex3f(-2, 0,-2)
        glVertex3f(-2, 0, 2)
        glVertex3f( 2, 0, 2)
        glVertex3f( 2, 0,-2)
        glEnd()
        glEnable(GL_LIGHTING)

    def displayScene(s):
        "Tout l'affichage se fait ici"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # on se recule (sinon on a le nez dans le lavabo)
        glTranslate(0,0,-8)
        # on tourne selon l'axe vertical, facile
        glRotate(s.lon,0,1.0,0)
        # on tourne selon un compromis entre l'axe x et l'axe z pour lever la caméra
        glRotate(s.lat,cos(d2r*s.lon),0,sin(d2r*s.lon)) #

        if s.mode==Mode.visualise:
            glPushMatrix()
            glRotate(s.plon,1,0,0)
            glRotate(s.plat,0,cos(d2r*s.plon),sin(d2r*s.plon))
            glTranslate(0,s.phau,0)
            s.poly()
            glPopMatrix()
        
        if s.mode==Mode.squelette:
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
                
        if s.mode>Mode.squelette:
            glColor3f(1,1,1)
            for l in s.imppoints:
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

    def mouse(s,but,state,x,y):
        if but==GLUT_LEFT_BUTTON and state==GLUT_DOWN:
            s.xOld=x
            s.yOld=y
        elif but in (3,4) and s.mode==Mode.visualise:
            s.phau += 0.04 if but==4 else -0.04
            s.phau = (s.phau+1.8)%3.6 - 1.8
            glutPostWindowRedisplay(s.wVisu)
            glutPostRedisplay()
        

    def move(s,x,y):
        if s.mode==Mode.visualise:
            s.xOld, s.plon = x, (s.plon+x-s.xOld)%360
            s.yOld, s.plat = y, (s.plat+y-s.yOld)%360
            glutPostWindowRedisplay(s.wVisu)
        else:
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


