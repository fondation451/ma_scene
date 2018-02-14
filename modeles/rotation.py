from math import cos,sin

# Rotation atour de x
def __compute_anim(p, ident, t):
    theta = 0.1 * t
    costheta = cos(theta)
    sintheta = sin(theta)
    x = p[0]
    y = p[1] * costheta - p[2] * sintheta
    z = p[1] * sintheta + p[2] * costheta
    new_p = [x, y, z]
    return new_p
