from obj import litObj
from implicit import Implicit
from sys import argv, stdout
from pickle import dump


points,lines,faces = litObj(argv[1])

# Traitement des surfaces implicites
####

Ri = 1
ki = 10.0
iso = 3
eps = 0.3
step_cube = 1

implicit = Implicit(points, lines, Ri, ki, iso, eps, step_cube)
#iprint("Points du squelette\n")
#print(points)
implicit_points = implicit.compute()

#print("Points de la surface implicite\n")
#print(implicit_points)

####

dump((points,lines,faces),stdout.buffer)
dump(implicit_points,stdout.buffer)

