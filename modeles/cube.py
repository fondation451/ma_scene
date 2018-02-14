from sys import argv, stdout,stderr

def __compute_anim(p, ident, t):
    k1 = 0.1 * t
    if ident == "s1":
        new_p = [p[0] + k1, p[1] + k1,  p[2] + k1]
    elif ident == "s2":
        new_p = [p[0] - k1, p[1] - k1,  p[2] - k1]
    else:
        new_p = p
    return new_p
