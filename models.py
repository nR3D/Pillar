import numpy as np
from renderer import transform_matrix

class Obj():
    def __init__(self, vertices : list, faces=[], lines=[], **kwargs):
        self.vertices = vertices
        self.faces = faces
        self.INDEX_OFFSET : int = kwargs['INDEX_OFFSET'] if 'INDEX_OFFSET' in kwargs else 1
        self.WIREFRAME : bool = kwargs['WIREFRAME'] if 'WIREFRAME' in kwargs else False
        self.DRAW_VERTICES : bool = kwargs['DRAW_VERTICES'] if 'DRAW_VERTICES' in kwargs else False

    def to_camera(self, camera : np.matrix) -> list:
        """
        Return vertices position modified according to the 
        camera coordinate system.
        """
        points_camera = list()
        # transformation is applied to the camera, so the object will have an inverted view
        camera = transform_matrix({'matrix':camera, 'scaling':(1,1,1)})
        for vertex in self.vertices:
            p_camera = camera.dot(vertex)
            points_camera.append(p_camera.A1)
        return points_camera

    def _apply_vertices(self, matrix) -> None:
        """
        Iter through self.vertices to apply a matrix tranformation
        """
        transformed_vertices = list()
        for vertex in self.vertices:
            transformed_vertices.append(matrix.dot(vertex))
        self.vertices = transformed_vertices

    def transform(self, op={}) -> None:
        """
        A unique wrapper for tranlsation, rotation, and scaling.
        e.g self.transform({'translation': (xt, yt, zt), 
                            'rotation': (xr, yr, zr),
                            'scaling': (xs, ys, zs)})
        """
        transformation_matrix = transform_matrix(op)
        self._apply_vertices(transformation_matrix)

    def translate(self, x, y, z) -> None:
        translation_matrix = transform_matrix({'translation': (x,y,z)})
        self._apply_vertices(translation_matrix)
    
    def rotate(self, x, y, z) -> None:
        rotation_matrix = transform_matrix({'rotation':(x,y,z)})
        self._apply_vertices(rotation_matrix)

    def scale(self, x, y, z) -> None:
        scaling_matrix = transform_matrix({'scaling':(x,y,z)})
        self._apply_vertices(scaling_matrix)
