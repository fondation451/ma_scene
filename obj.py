from sys import argv, stdout,stderr

def litObj(chemin, Ri, ki):
    vec,lig,faces = [],[],[]
    kip = []
    Rip = []
    coef = []
    ids = []
    with open(chemin) as f:
        for s in f:
            if s[0]=="#": continue
            l = s.split(" ")
            if l[0]=="v":
                vec.append((float(l[1]),float(l[2]),float(l[3])))
                try:
                    Rip.append(float(l[6]))
                except IndexError:
                    Rip.append(Ri)

                try:
                    kip.append(float(l[7]))
                except IndexError:
                    kip.append(ki)

                try:
                    coef.append(float(l[5]))
                except IndexError:
                    coef.append(1.0)

                try:
                    ids.append(l[4].rstrip())
                except IndexError:
                    ids.append("no")
            if l[0]=="l":
                lig.append((int(l[1]),int(l[2])))
            elif l[0]=="f":
                face = tuple(tuple(map(lambda x: int(x) if x else 0, p.split("/"))) for p in l[1:])
                faces.append(face)

    return vec,lig,faces,Rip,kip,coef,ids


def litAnim(chemin):
    with open(chemin) as f:
        content = f.read()
        return content
