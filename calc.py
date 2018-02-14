from obj import litObj, litAnim
from implicit import Implicit
from sys import argv, stdout,stderr
from pickle import dump

Ri = 0.1
ki = 10.0
iso = 3
eps = 0.3
nb_cubes = 60 # cubes par côté
t_end = 50

points,lines,faces,Rip,kip,coef,ids = litObj(argv[1], Ri, ki)

print(points, file=stderr)
print(lines, file=stderr)
print(faces, file=stderr)
print(Rip, file=stderr)
print(kip, file=stderr)
print(coef, file=stderr)
print(ids, file=stderr)

anim_fun = litAnim(argv[2])
exec(anim_fun, globals())

def update_frame(points, ids, t):
    new_points = []
    for i in range(0, len(points)):
        new_points.append(__compute_anim(points[i], ids[i], t))

    return new_points

def animation_of(points, ids, t_end):
    out = []
    for t in range(0, t_end + 1):
        new_points = update_frame(points, ids, t)
        implicit = Implicit(new_points, lines, faces, Rip, kip, coef, iso, nb_cubes)
        implicit_points = implicit.compute()
        out.append((new_points, implicit_points))

    return out

# Traitement des surfaces implicites
####

animation = animation_of(points, ids, t_end)

####

dump((lines,faces),stdout.buffer)
dump(animation,stdout.buffer)
