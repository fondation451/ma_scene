from obj import litObj
from implicit import Implicit
from sys import argv, stdout,stderr
from pickle import dump

Ri = 0.1
ki = 10.0
iso = 3
nb_cubes = 40 # cubes par côté

points,lignes,faces,Rip,kip,coef = litObj(argv[1], Ri, ki)

#print(ki_points, file=stderr)
#print(Ri_points, file=stderr)
#print(Ri_lines, file=stderr)
#print(ki_lines, file=stderr)

# Traitement des surfaces implicites
####
implicit = Implicit(points, lignes, faces, Rip, kip, coef, iso, nb_cubes)

#iprint("Points du squelette\n")
#print(points)
implicit_points = implicit.compute()

#print("Points de la surface implicite\n")
#print(implicit_points)

####

dump((points,lignes,faces),stdout.buffer)
dump(implicit_points,stdout.buffer)

