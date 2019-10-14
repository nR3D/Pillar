import numpy as np
from renderer import transform_matrix

class Obj():
    def __init__(self, vertices : list, faces=[], lines=[], **kwargs):
        self.vertices = vertices
        self.faces = faces
        self.INDEX_OFFSET : int = kwargs.get('INDEX_OFFSET', 1)
        self.WIREFRAME : bool = kwargs.get('WIREFRAME', False)
        self.DRAW_VERTICES : bool = kwargs.get('DRAW_VERTICES', False)

    def iter_vertices(self, matrix : np.matrix) -> None:
        """
        Iter through self.vertices to apply a matrix tranformation
        """
        transformed_vertices = list()
        for vertex in self.vertices:
            transformed_vertices.append(matrix.dot(vertex).A1)
        return transformed_vertices

    def transform(self, **kwargs) -> None:
        """
        A unique wrapper for tranlsation, rotation, and scaling.
        e.g self.transform(translation=(xt, yt, zt), 
                           rotation=(xr, yr, zr),
                           scaling=(xs, ys, zs))
        """
        transformation_matrix = transform_matrix(kwargs=kwargs)
        self.vertices = self.iter_vertices(transformation_matrix)

    def translate(self, x, y, z) -> None:
        translation_matrix = transform_matrix(translation=(x,y,z))
        self.vertices = self.iter_vertices(translation_matrix)

    def rotate(self, x, y, z) -> None:
        rotation_matrix = transform_matrix(rotation=(x,y,z))
        self.vertices = self.iter_vertices(rotation_matrix)

    def scale(self, x, y=None, z=None) -> None:
        if y is None:
            y = x
        if z is None:
           z = y
        scaling_matrix = transform_matrix(scaling=(x,y,z))
        self.vertices = self.iter_vertices(scaling_matrix)

