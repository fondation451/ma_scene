from os import popen
from obj import litObj
from implicit import Implicit
from sys import argv, stdout,stderr
from pickle import dump, load
from scene import Scene

if len(argv)==1:
    argv.append("modeles/cube.obj")
if len(argv)!=2:
    print("Utilisation: ma_scene.py scene.obj")
    exit(1)

if argv[1].endswith(".pts"):
    with open(argv[1],"rb") as f:
        points,lignes,faces = load(f)
        implicit_points = load(f)
    implicit = None
else:
    Ri = 0.1
    ki = 10.0
    iso = 3
    nb_cubes = 10 # cubes par côté

    points,lignes,faces,Rip,kip,coef = litObj(argv[1], Ri, ki)

    implicit = Implicit(points, lignes, faces, Rip, kip, coef, iso, nb_cubes)

    implicit_points = implicit.compute()

    with open("last.pts","wb") as f:
        dump((points,lignes,faces),f)
        dump(implicit_points,f)

scene = Scene(points,lignes,faces,implicit_points, implicit)
scene.main()

