# Fonctions pour les surfaces implicites

from math import exp,sqrt,fabs

class Implicit:
    def __init__(self, points, Ri, ki, iso, eps, step_line, step_cube):
        self.points = points
        self.Ri = Ri
        self.ki = ki
        self.iso = iso
        self.eps = eps
        self.step_line = step_line
        self.step_cube = step_cube


    def dist(self, p1, p2):
        X1 = p1[0] - p2[0]
        Y1 = p1[1] - p2[1]
        Z1 = p1[2] - p2[2]
        return sqrt(X1 * X1 + Y1 * Y1 + Z1 * Z1)


    def fi(self, i, P):
        distance = self.dist(self.points[i], P)
        return self.ki * exp(-1 * distance * distance / (self.Ri * self.Ri))


    def f(self, P):
        out = 0
        for i in range(0, len(self.points)):
            out = out + self.fi(i, P)
        return out


    def fiso(self, P):
        return fabs(self.f(P) - self.iso)


    def check(self, P):
        return self.iso - self.f(P) <= self.eps


    # Calcule le vecteur de P1P2 dont la taille est step_line fois moins grande que le vecteur P1P2
    def vecteur_dir(self, p1, p2, step_line):
        x = p2[0] - p1[0]
        y = p2[1] - p1[1]
        z = p2[2] - p1[2]
        return [x/step_line, y/step_line, z/step_line]


    def add_vec(self, v1, v2):
        return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]


    # Verifie si la surface implicite s'intersecte avec un segment
    def intersection_line(self, p1, p2):
        vect_dir = self.vecteur_dir(p1, p2, self.step_line)
        p_min = []
        p_min_val = 10
        p_curr = p1
        for i in range(0, int(self.step_line) + 1):
            tmp = self.fiso(p_curr)
#            print(p_curr,tmp)
            if tmp <= self.eps:
                if p_min == [] or p_min_val > tmp:
                    p_min = p_curr
                    p_min_val = tmp
            p_curr = self.add_vec(p_curr, vect_dir)

        return p_min


    # Renvoie tous les points qui s'intersectent avec un cube
    # c est le coin en haut à gauche en premier plan
    def intersection_cube(self, c):
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
        if P1 != []: out.append(P1)
        if P2 != []: out.append(P2)
        if P3 != []: out.append(P3)
        if P4 != []: out.append(P4)
        if P5 != []: out.append(P5)
        if P6 != []: out.append(P6)
        if P7 != []: out.append(P7)
        if P8 != []: out.append(P8)
        if P9 != []: out.append(P9)
        if P10 != []: out.append(P10)
        if P11 != []: out.append(P11)
        if P12 != []: out.append(P12)
        return out


    def compute_enveloppe(self):
        mult = 3
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
        longueur = (x_max - x_min) * mult
        largeur = (y_max - y_min) * mult
        profondeur = (z_max - z_min) * mult
        c = [x_min * mult, y_min * mult, z_min * mult]
        # cote de l'enveloppe parallélépipédique en bas à gauche premier plan
        return (c, longueur, largeur, profondeur)


    # Calcule la surface implicite
    def compute(self):
        out_points = []
        out_face = []
        ind_point = 0
        (c_env, lon_env, lar_env, pro_env) = self.compute_enveloppe()

        step_lon = lon_env / self.step_cube
        step_lar = lar_env / self.step_cube
        step_pro = pro_env / self.step_cube
        w=0
        for i in range(0, int(step_lon) + 1):
            c_x = c_env[0] + self.step_cube * i
            for j in range(0, int(step_lar) + 1):
                c_y = c_env[1] + self.step_cube * j
                for k in range(0, int(step_pro) + 1):
#                    if (i+j+k)%2: continue
                    c_z = c_env[2] + self.step_cube * k
                    new_points = self.intersection_cube([c_x, c_y, c_z])
                    if new_points:
                        out_points.append(self.points_to_poly(new_points))
        return out_points

    # Ordonne une liste de sommets pour en faire un polygône
    # Semble fonctionner souvent mais il reste qq trous dans la surface
    def points_to_poly(self, l):
        if len(l)<4: return l
        l2 = [l[0]]
        l.remove(l[0])
        while l:
            point = l2[-1]
            nearest = min(l, key = lambda p:self.dist(p,point))
            l.remove(nearest)
            l2.append(nearest)
        return l2
