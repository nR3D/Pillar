from PIL import Image, ImageDraw
import numpy as np
from models import Obj
from importer import import_obj
from renderer import transform_matrix, render
    
if __name__ == "__main__":
    v1 = np.array([-10, -10, -10, 1])
    v2 = np.array([10, -10, -10, 1])
    v3 = np.array([10, -10, 10, 1])
    v4 = np.array([-10, -10, 10, 1])
    v5 = np.array([-10, 10, -10, 1])
    v6 = np.array([10, 10, -10, 1])
    v7 = np.array([10, 10, 10, 1])
    v8 = np.array([-10, 10, 10, 1])
    o1 = Obj([v1,v2,v3,v4,v5,v6,v7,v8], faces=[(1,2,3,4),(1,5,8,4),(6,7,3,2),(5,6,2,1),(5,6,7,8),(8,7,3,4)], WIREFRAME=True, DRAW_VERTICES=True)
    o2 = Obj([v1,v2,v3], faces=[(1,2,3)])
    #oi = import_obj('./objs/tree.obj')
    coordinate_system = transform_matrix({'rotation':(0,120,0), 'translation':(0,0,-50), 'scaling':(1,1,1)})
    print("Camera coordinate system:", coordinate_system, sep='\n')
    render(coordinate_system, [o1,])
    
