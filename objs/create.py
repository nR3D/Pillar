from models import Obj
from math import pi, cos, sin

def cylinder(radius=1, height=5, segments=20, inner_radius=0):
    """
    Create a cylinder, segments must be at least 3
    """
    vertices = list()
    faces = list()
    angle = 2*pi/segments
    for i in range(segments+1):
        vertices.append((radius*cos(angle*i), height/2, radius*sin(angle*i), 1))
        vertices.append((radius*cos(angle*i), -height/2, radius*sin(angle*i), 1))
        vertices.append((inner_radius*cos(angle*i), height/2, inner_radius*sin(angle*i), 1))
        vertices.append((inner_radius*cos(angle*i), -height/2, inner_radius*sin(angle*i), 1))
        if i:
            offset = (i-1)*4
            mod = offset+4 if i == segments else 0 
            faces.append((offset+1, offset+3, offset+7-mod, offset+5-mod))  # connect upper vertices
            faces.append((offset+2, offset+4, offset+8-mod, offset+6-mod))  # connect lower vertices
            faces.append((offset+1, offset+2, offset+6-mod, offset+5-mod))  # connect extern vertices
            faces.append((offset+3, offset+4, offset+8-mod, offset+7-mod))  # connect inner vertices
    return Obj(vertices, faces)

def cube(x, y=None, z=None):
    if y is None:
        y = x
    if z is None:
        z = y
    vertices = ((x, -y, -z, 1), (-x, -y, -z, 1), (-x, y, -z, 1), (x, y, -z, 1),
                (x, -y, z, 1), (-x, -y, z, 1), (-x, y, z, 1), (x, y, z, 1))
    faces = ((1,2,3,4), (1,4,8,5), (5,6,7,8), (6,7,3,2), (3,4,8,7), (1,2,6,5))
    return Obj(vertices, faces)

