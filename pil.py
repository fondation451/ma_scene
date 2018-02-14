import PIL.Image as pim
from pickle import load

with open("slice.pts","rb") as f:
    l = load(f)

def couleur(v):
    v = (v-mn)/(mx-mn)
    v = v**0.4
    if v%0.05>0.045:
        return 255,255,255
    elif v<0.5:
        return 0,0,int(256*v*2)
    else:
        return 0,int(256*v*2-256),int(512-256*v*2)
        
im = pim.new("RGB",(len(l),len(l[0])))
mn = min(min(c) for c in l)
mx = max(max(c) for c in l)

for x,c in enumerate(l):
    for y,v in enumerate(c):
        im.putpixel((x,y),couleur(v))

im.resize((1000,1000),resample=pim.LANCZOS).show()
        
