# Fonctions pour les surfaces implicites

from math import exp,sqrt,fabs,pi,cos,sin
import numpy as np
from time import time
from sys import stderr
from multiprocessing import Pool
from random import shuffle

# Calcule le vecteur de P1P2 dont la taille est step_line fois moins grande que le vecteur P1P2
def vecteur_dir(p1, p2, step_line):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    z = p2[2] - p1[2]
    return [x/step_line, y/step_line, z/step_line]


class Implicit:
    def __init__(self, points, lignes, Ri, ki, iso, eps, step_cube):
        self.points = points
        self.lignes = []
        self.Ri = Ri
        self.ki = ki
        self.iso = iso
        self.eps = eps
        self.step_cube = step_cube
        self.ar = 0
        self.inter = {}

        # Init lignes
        for l in lignes:
            i = l[0] - 1
            j = l[1] - 1
            a = self.points[i]
            b = self.points[j]
            vect_dir = vecteur_dir(a, b, 1)
            norm_v = np.linalg.norm(vect_dir)
            vect_dir = [vect_dir[0]/norm_v, vect_dir[1]/norm_v, vect_dir[2]/norm_v]
            self.lignes.append((a, vect_dir))
        print("Lignes :", file=stderr)
        print(len(self.lignes), file=stderr)


    def dist(self, p1, p2):
        X1 = p1[0] - p2[0]
        Y1 = p1[1] - p2[1]
        Z1 = p1[2] - p2[2]
        return sqrt(X1 * X1 + Y1 * Y1 + Z1 * Z1)


    def fi(self, i, P):
        distance = self.dist(self.points[i], P)
        return self.ki * exp(-1 * distance * distance / (self.Ri * self.Ri))


    def fi_lines(self, a, u, P):
#        print("CALL fi_lines", file=stderr)
        aP = [P[0] - a[0], P[1] - a[1], P[2] - a[2]]
#        cross_prod = np.cross(p1P, vec_dir)
        cross_prod = np.cross(aP, u)
#        cross_prod = [0.5, 0.5, 0.5]
#        print("vec_dir = ", file=stderr)
#        print(vec_dir, file=stderr)
#        print("cross_prod = ", file=stderr)
#        print(cross_prod, file=stderr)
        distance = np.linalg.norm(cross_prod)
        return self.ki * exp(-1 * distance * distance / (self.Ri * self.Ri))
#        return 0.0

    def f(self, P):
#        print("CALL of f", file=stderr)
        out = 0
        for i in range(0, len(self.points)):
            out = out + self.fi(i, P)

        for l in self.lignes:
            (a, u) = l
            out = out + self.fi_lines(a, u, P)

        return out


    def fiso(self, P):
        return fabs(self.f(P) - self.iso)


    def check(self, P):
        return self.iso - self.f(P) <= self.eps


    def add_vec(self, v1, v2):
        return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]


    def intersection_line(self, p1, p2):
        " Verifie si la surface implicite s'intersecte avec un segment "
        p1 = tuple(p1)
        p2 = tuple(p2)
        if (p1,p2) in self.inter:
            return self.inter[(p1,p2)]
        if (p2,p1) in self.inter:
            return self.inter[(p2,p1)]
        v1 = self.f(p1)
        v2 = self.f(p2)
        c1 = v1>self.iso
        c2 = v2>self.iso
        if not (c1 ^ c2): return []
        l = self.dist(p1,p2)
        if c2:
            d = (self.iso-v1)/(v2-v1)
            r = self.add_vec(p1,vecteur_dir(p1,p2,1/(l*d)))
        else:
            d = (self.iso-v2)/(v1-v2)
            r = self.add_vec(p2,vecteur_dir(p2,p1,1/(l*d)))
        self.inter[(p1,p2)] = r
        return r


    def intersection_cube(self, c):
        """ Renvoie tous les points qui s'intersectent avec un cube
            c est le coin en haut à gauche en premier plan """
        out = []
        x = self.step_cube # longueur du cote du cube
        p1 = c
        p2 = self.add_vec(c, [x, 0, 0])
        p3 = self.add_vec(c, [x, 0, x])
        p4 = self.add_vec(c, [0, 0, x])
        p5 = self.add_vec(c, [0, x, 0])
        p6 = self.add_vec(c, [x, x, 0])
        p7 = self.add_vec(c, [x, x, x])
        p8 = self.add_vec(c, [0, x, x])
        P1 = self.intersection_line(p1, p2)
        P2 = self.intersection_line(p1, p4)
        P3 = self.intersection_line(p1, p5)
        P4 = self.intersection_line(p2, p3)
        P5 = self.intersection_line(p2, p6)
        P6 = self.intersection_line(p3, p4)
        P7 = self.intersection_line(p3, p7)
        P8 = self.intersection_line(p4, p8)
        P9 = self.intersection_line(p5, p6)
        P10 = self.intersection_line(p5, p8)
        P11 = self.intersection_line(p6, p7)
        P12 = self.intersection_line(p7, p8)
        if P1 != []: out.append((1,P1))
        if P2 != []: out.append((2,P2))
        if P3 != []: out.append((3,P3))
        if P4 != []: out.append((4,P4))
        if P5 != []: out.append((5,P5))
        if P6 != []: out.append((6,P6))
        if P7 != []: out.append((7,P7))
        if P8 != []: out.append((8,P8))
        if P9 != []: out.append((9,P9))
        if P10 != []: out.append((10,P10))
        if P11 != []: out.append((11,P11))
        if P12 != []: out.append((12,P12))
        return out

    def compute_enveloppe(self):
        marge = 1.5 * self.Ri
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        z_min = 0
        z_max = 0
        for p in self.points:
            if p[0] < x_min: x_min = p[0]
            if p[0] > x_max: x_max = p[0]
            if p[1] < y_min: y_min = p[1]
            if p[1] > y_max: y_max = p[1]
            if p[2] < z_min: z_min = p[2]
            if p[2] > z_max: z_max = p[2]
        longueur = x_max - x_min + 2 * marge
        largeur  = y_max - y_min + 2 * marge
        profondeur = z_max - z_min + 2 * marge
        c = [x_min - marge, y_min - marge, z_min - marge]
        # cote de l'enveloppe parallélépipédique en bas à gauche premier plan
        return (c, longueur, largeur, profondeur)

    def compute_cube(self, arg):
        c_env, lon_env, lar_env, pro_env = arg
        " Calcule la surface implicite dans le pavé donné en entrée "
        out_points = []
        out_cubes = []
        ind_point = 0

        step_lon = lon_env / self.step_cube
        step_lar = lar_env / self.step_cube
        step_pro = pro_env / self.step_cube
        num = int(step_lon)*int(step_lar)*int(step_pro)
        cub = 0
        for i in range(0, int(step_lon)):
            c_x = c_env[0] + self.step_cube * i
            for j in range(0, int(step_lar)):
                c_y = c_env[1] + self.step_cube * j
                for k in range(0, int(step_pro)):
                    cub += 1
                    c_z = c_env[2] + self.step_cube * k
                    print("\r",cub,"/",num,"  ",end="",file=stderr)
                    new_points = self.intersection_cube([c_x, c_y, c_z])
                    if new_points:
                        out_cubes.append(([c_x, c_y, c_z], self.step_cube,
                                          self.step_cube, self.step_cube))
                        out_points.append(self.points_to_poly(new_points))
        return out_cubes, out_points

    def compute(self):
#        print("CALL compute", file=stderr)
        t = time()
        env = [self.compute_enveloppe()]
#        print("env", file=stderr)
#        print(env, file=stderr)
        with Pool(6) as pool:
            for _ in range(1):
                cubes, points = [], []
 #               print("env", file=stderr)
 #               print(env, file=stderr)
                self.step_cube = env[0][1]/20
                res = pool.map(self.compute_cube, env)
                for cub,pts in res:
                    points.extend([[(p,self.normal_at(p)) for p in l]for l in pts])
                    cubes.extend(cub)
                env = cubes
 #               print("points", file=stderr)
 #               print(points, file=stderr)
        print(time()-t, self.ar, file=stderr)
        return points

    def normal_at(self, point):
        d2r = 2*pi/360
        l = 0.01
        m, pm = 100, None
        for i in range(0,360,30):
            for j in range(0,360,30):
                pn = (cos(i*d2r)*cos(j*d2r),sin(i*d2r)*cos(j*d2r),sin(j*d2r))
                v = self.f(self.add_vec(point,(pn[0]*l,pn[1]*l,pn[2]*l)))
                if v<m: m, pm = v, pn
        return pm
    
    def points_to_poly(self, l):
        """ Ordonne une liste de sommets pour en faire un polygône
            Semble fonctionner souvent mais il reste qq trous dans la surface """
        faces = [(1,4,6,2),(1,5,9,3),(2,8,10,3),(4,7,11,5),(6,8,12,7),(9,11,12,10)]
        adjacent = [[], [4, 6, 2, 5, 9, 3], [1, 4, 6, 8, 10, 3], [1, 5, 9, 2, 8, 10],
                   [1, 6, 2, 7, 11, 5], [1, 9, 3, 4, 7, 11], [1, 4, 2, 8, 12, 7],
                   [4, 11, 5, 6, 8, 12], [2, 10, 3, 6, 12, 7], [1, 5, 3, 11, 12, 10],
                   [2, 8, 3, 9, 11, 12], [4, 7, 5, 9, 12, 10], [6, 8, 7, 9, 11, 10]]
        if len(l)<=3:
        #shuffle(l)
            return [p for f,p in l] # inutile d'ordonner les sommets d'un triangle
        l2 = [l[0]]
        l.remove(l[0])
        while l:
            face, point = l2[-1]
            try:
                nearest = min(filter(lambda f: f[0] in adjacent[face], l),
                              key = lambda p: self.dist(p[1],point))
            except:
                return []
            l.remove(nearest)
            l2.append(nearest)
        return [p for f,p in l2]
