from obj import litObj
from implicit import Implicit
from sys import argv, stdout,stderr
from pickle import dump

Ri = .05
#ki = 10.0
ki = 2.0
#iso = 3
iso = 1
eps = 0.3
nb_cubes = 30 # cubes par côté

points,lines,faces,Rip,kip = litObj(argv[1], Ri, ki)

#print(ki_points, file=stderr)
#print(Ri_points, file=stderr)
#print(Ri_lines, file=stderr)
#print(ki_lines, file=stderr)

# Traitement des surfaces implicites
####

implicit = Implicit(points, lines, Rip, kip, iso, eps, nb_cubes)
#iprint("Points du squelette\n")
#print(points)
implicit_points = implicit.compute()

#print("Points de la surface implicite\n")
#print(implicit_points)

####

dump((points,lines,faces),stdout.buffer)
dump(implicit_points,stdout.buffer)

