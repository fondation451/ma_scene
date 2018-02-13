from obj import litObj
from implicit import Implicit
from sys import argv, stdout
from pickle import dump


points,lines,faces = litObj(argv[1])

# Traitement des surfaces implicites
####

Ri = .3
ki = 10.0
iso = 3
eps = 0.3
nb_cubes = 30 # cubes par côté

implicit = Implicit(points, lines, Ri, ki, iso, eps, nb_cubes)
#iprint("Points du squelette\n")
#print(points)
implicit_points = implicit.compute()

#print("Points de la surface implicite\n")
#print(implicit_points)

####

dump((points,lines,faces),stdout.buffer)
dump(implicit_points,stdout.buffer)

