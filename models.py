import numpy as np

class CoordinateSystem():
    def __init__(self, matrix=np.ones((4,4))):
        self.matrix = matrix
    def __str__(self):
        return self.matrix.__str__()

from renderer import transform_matrix

class Obj():
    def __init__(self, vertices : list, faces=[], lines=[]):
        self.vertices = vertices
        self.faces = faces
        self._INDEX_OFFSET = 1
    def to_camera(self, camera : CoordinateSystem) -> list:
        points_camera = list()
        for vertex in self.vertices:
            p_camera = camera.matrix.dot(vertex)
            points_camera.append(p_camera.A1)
        return points_camera
    def translate(self, x, y, z):
        translate_matrix = transform_matrix({'translation': (x,y,z)})
        for vertex in self.vertices:
            vertex = translate_matrix.dot(vertex)