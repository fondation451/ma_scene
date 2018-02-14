def __compute_anim(p, ident, t):
    k1 = 0.1 * t
    if ident == "p":
      new_p = [p[0], p[1] - k1 ,p[2]]
    else:
        new_p = p
    return new_p
