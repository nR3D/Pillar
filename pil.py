from importer import import_obj
from renderer import transform_matrix, render
from objs.create import *
    
if __name__ == "__main__":
    o2 = cylinder(height=0.1, radius=3, inner_radius=1.7, segments=100)
    o2.rotate(0,0,10)
    oi = import_obj('./objs/pumpkin.obj')
    oi.scale(1)
    plane = cube(10,0.1,2)
    coordinate_system = transform_matrix(rotation=(20,0,0), translation=(0,-2,-7), scaling=(1,1,1))
    print("Camera coordinate system:", coordinate_system, sep='\n')
    render(coordinate_system, [oi,plane], WIREFRAME=False, DRAW_VERTICES=False, SOLID=True)
    
