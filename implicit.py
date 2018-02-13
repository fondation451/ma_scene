# Fonctions pour les surfaces implicites

from math import exp,sqrt,fabs,pi,cos,sin
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
    def __init__(self, points, lignes, Rip, kip, iso, eps, nb_cubes):
        self.points = points
        self.lignes = []
        self.Rip = Rip
        self.kip = kip
        self.Ril = []
        self.kil = []
        self.iso = iso
        self.eps = eps
        self.nb_cubes = nb_cubes
        self.inter = {}

        # Init lignes
        for l in lignes:
            i = l[0] - 1
            j = l[1] - 1
            a = self.points[i]
            b = self.points[j]
            Ripi = self.Rip[i]
            kipi = self.kip[i]
            Ripj = self.Rip[j]
            kipj = self.kip[j]
            Riline = (Ripi + Ripj) / 2
            kiline = (kipi + kipj) / 2
            vect_dir = vecteur_dir(a, b, 1)
            norm_v = self.dist((0,0,0),vect_dir)
            vect_dir = [vect_dir[0]/norm_v, vect_dir[1]/norm_v, vect_dir[2]/norm_v]
            self.lignes.append((a, b, vect_dir))
            self.Ril.append(Riline)
            self.kil.append(kiline)
        print("Lignes :", file=stderr)
        print(len(self.lignes), file=stderr)


    def dist(self, p1, p2):
        X1 = p1[0] - p2[0]
        Y1 = p1[1] - p2[1]
        Z1 = p1[2] - p2[2]
        return sqrt(X1 * X1 + Y1 * Y1 + Z1 * Z1)


    def fi(self, i, P):
        distance = self.dist(self.points[i], P)
        Ri = self.Rip[i]
        ki = self.kip[i]
        return ki * exp(-1 * distance * distance / (Ri * Ri))

    def fi_lines(self, i, p):
        " Valeur du champ du segment [ab] de droite u en p "
        (a, b, u) = self.lignes[i]
        ap = (p[0] - a[0], p[1] - a[1], p[2] - a[2])
        bp = (p[0] - b[0], p[1] - b[1], p[2] - b[2])
        uSap = u[0]*ap[0]+u[1]*ap[1]+u[2]*ap[2]
        uSbp = u[0]*bp[0]+u[1]*bp[1]+u[2]*bp[2]
        if uSap > 0 and uSbp < 0:
            cross = (ap[1]*u[2] - ap[2]*u[1],
                     ap[2]*u[0] - ap[0]*u[2],
                     ap[0]*u[1] - ap[1]*u[0])
            distance = sqrt(cross[0]**2+cross[1]**2+cross[2]**2)
        else:
            distance = min(self.dist(a,p),self.dist(b,p))
        Ri = self.Ril[i]
        ki = self.kil[i]
        return ki * exp(-1 * distance * distance / (Ri * Ri))

    def f(self, P):
        out = 0
        for i in range(0, len(self.points)):
            out = out + self.fi(i, P)

        for i in range(0, len(self.lignes)):
            out = out + self.fi_lines(i, P)

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
        l = (p1,p2)
        v1 = self.f(p1)
        v2 = self.f(p2)
        c1 = v1>self.iso
        c2 = v2>self.iso
        if not (c1 ^ c2): return []
        if c2: p1,p2,v1,v2=p2,p1,v2,v1
        for _ in range(5):
            d = (self.iso-v2)/(v1-v2)
            p = self.add_vec(p2,vecteur_dir(p2,p1,1/d))
            v = self.f(p)
            if v>self.iso:
                p1,v1=p,v
            else:
                p2,v1=p,v
        self.inter[l] = p
        return p
 

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
        Ri = max(self.Rip)
        marge = 3 * Ri
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
        num = int(step_lon+1)*int(step_lar+1)*int(step_pro+1)
        cub = 0
        for i in range(0, int(step_lon)+1):
            c_x = c_env[0] + self.step_cube * i
            for j in range(0, int(step_lar)+1):
                c_y = c_env[1] + self.step_cube * j
                print("\r",cub,"/",num,"  ",end="",file=stderr)
                for k in range(0, int(step_pro)+1):
                    cub += 1
                    c_z = c_env[2] + self.step_cube * k
                    new_points = self.intersection_cube([c_x, c_y, c_z])
                    if new_points:
                        out_cubes.append(([c_x, c_y, c_z], self.step_cube,
                                          self.step_cube, self.step_cube))
                        out_points.append(self.points_to_poly(new_points))
        print("\r",len(out_cubes),"non-vides sur",cub,"   ",file=stderr)
        return out_cubes, out_points

    def compute(self):
        print("Calcul surface", file=stderr)
        t = time()
        env = [self.compute_enveloppe()]
        cubes, points = [], []
        self.step_cube = env[0][1]/self.nb_cubes
        res = map(self.compute_cube, env)
        for cub,pts in res:
            points.extend(pts)
            cubes.extend(cub)
        env = cubes
        print("",round(time()-t,3),"s", file=stderr)
        print("Calcul normales", file=stderr)
        t=time()
        num = len(points)
        norm = [None]*num
        for i,l in enumerate(points):
            if not i%43: print("\r",i,"/",num,"  ",end="",file=stderr)
            #norm[i] = [(p,p) for p in l] # pour passer le calcul
            norm[i] = [(p,self.normal_at(p)) for p in l]
        print("\r",round(time()-t,3),"s     ", file=stderr)
        return norm
    
    def normal_at(self, point):
        d2r = 2*pi/360
        l = 0.01
        m, pm = 100, None
        for i in range(0,360,60):
            for j in range(0,360,60):
                pn = (cos(i*d2r)*cos(j*d2r),sin(i*d2r)*cos(j*d2r),sin(j*d2r))
                v = self.f(self.add_vec(point,(pn[0]*l,pn[1]*l,pn[2]*l)))
                if v<m: m, im, jm = v, i, j
        m = 100
        for i in range(im-30,im+30,9):
            for j in range(jm-30,jm+30,9):
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
