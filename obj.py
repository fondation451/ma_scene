def litObj(chemin):
    vec,lig,faces = [],[],[]
    with open(chemin) as f:
        for s in f:
            if s[0]=="#": continue
            l = s.split(" ")
            if l[0]=="v":
                vec.append((float(l[1]),float(l[2]),float(l[3])))
            if l[0]=="l":
                lig.append((int(l[1]),int(l[2])))
            elif l[0]=="f":
                face = tuple(tuple(map(lambda x: int(x) if x else 0, p.split("/"))) for p in l[1:])
                faces.append(face)
    return vec,lig,faces
