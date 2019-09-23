from PIL import Image, ImageDraw
import numpy as np
from models import CoordinateSystem, Obj
from importer import import_obj
from renderer import transform_matrix, render_pil, render_web
    
if __name__ == "__main__":
    cs = CoordinateSystem(np.matrix([[0.718762, 0.615033, -0.324214, 0],
                                    [-0.393732, 0.744416, 0.539277, 0],
                                    [0.573024, -0.259959, 0.777216, 0],
                                    [0.526967, 1.254234, -2.53215, 1]]))
    csw = CoordinateSystem(np.matrix([[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]]))
    v1 = np.array([-10, -10, -10, 1])
    v2 = np.array([10, -10, -10, 1])
    v3 = np.array([10, -10, 10, 1])
    v4 = np.array([-10, -10, 10, 1])
    v5 = np.array([-10, 10, -10, 1])
    v6 = np.array([10, 10, -10, 1])
    v7 = np.array([10, 10, 10, 1])
    v8 = np.array([-10, 10, 10, 1])
    o1 = Obj([v1,v2,v3,v4,v5,v6,v7,v8], faces=[(1,2,3,4),(1,5,8,4),(6,7,3,2),(5,6,2,1),(5,6,7,8),(8,7,3,4)])
    o2 = Obj([v1,v2,v3])
    # oi = import_obj('./objs/tree.obj')
    cst = CoordinateSystem(transform_matrix({'rotation':(0,0,0), 'translation':(0,0,0), 'scale':(1,1,1)}))
    print(cst)
    render_pil(cst, [o2,])
    
