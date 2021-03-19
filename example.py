from pillar import Renderer, Transformation, Obj
    
if __name__ == "__main__":
    pumpkin = Obj.from_file('./objs/pumpkin.obj')
    pumpkin.color = '#ffbb00'
    coordinate_system = Transformation()
    coordinate_system.apply(rotation=(20,0,0), translation=(0,-2,-7), scaling=(1,1,1))
    print("Camera coordinate system:", coordinate_system.matrix, sep='\n')
    Renderer(coordinate_system, [pumpkin,], WIREFRAME=False, SOLID=True, VERTICES=False).render()
