import numpy as np

class CoordinateSystem():
    def __init__(self, matrix=np.ones((4,4))):
        self.matrix = matrix
    def __str__(self):
        return self.matrix.__str__()

class Obj():
    def __init__(self, vertices : list, faces=[], lines=[]):
        self.vertices = vertices
        self.faces = faces
        self._INDEX_OFFSET = 1
    def to_camera(self, camera : CoordinateSystem) -> list:
        points_camera = list()
        for vertex in self.vertices:
            p_camera = vertex.dot(camera.matrix)
            points_camera.append(p_camera.A1)
        return points_camera