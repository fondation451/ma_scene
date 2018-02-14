from sys import stderr

def __compute_anim(p, ident, t):
    if t < 25:
        k = 0.1 * t
        if ident == "neg1" or ident == "neg2":
            new_p = [p[0] + k, p[1], p[2]]
        else:
            new_p = p

        return new_p
    else:
        t = t - 25
        k = 0.1 * t
        if ident == "neg1" or ident == "neg2":
            new_p = [p[0] + 2.5 - k, p[1], p[2]]
        else:
            new_p = p
        return new_p
