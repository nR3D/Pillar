import numpy as np
from pathlib import Path
from pillar.transformation import Transformation

class Obj():
    def __init__(self, vertices=[], faces=[], lines=[], color=None,
                 transformation=Transformation(), **kwargs):
        self.vertices = vertices
        self.faces = faces
        self.color = color
        self.transformation = transformation
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
        self.transformation.apply(kwargs=kwargs)

    def translate(self, x, y, z) -> None:
        self.transformation.translate()

    def rotate(self, x, y, z) -> None:
        self.transformation.rotate(x, y, z)

    def scale(self, x, y, z) -> None:
        self.transformation.scale(x, y, z)

    def apply_transformation(self, transformation) -> None:
        self.vertices = self.iter_vertices(self.transformation.matrix)
    
    @staticmethod
    def from_file(file_path : str):
        res_obj = Obj()
        for line in open(Path(file_path)):
            line = line.rstrip('\n').split(' ')
            if line[0] == 'v':
                res_obj.vertices.append(np.array([float(l) for l in line[1:] if l != '']))
                while len(res_obj.vertices[-1]) < 4:
                    res_obj.vertices[-1] = np.append(res_obj.vertices[-1],1)
            elif line[0] == 'f':
                # this implementation ignores vt and vn
                res_obj.faces.append([])
                for f in line[1:]:
                    if f != '':
                        res_obj.faces[-1].append(int(f.split('/')[0]))
        return res_obj
