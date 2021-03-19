import numpy as np

class Transformation():
    def __init__(self, initial_matrix = np.identity(4) ):
        self.matrix = initial_matrix

    def apply(self, **kwargs) -> None:
        if('translation' in kwargs):
            x, y, z = kwargs['translation']
            self.matrix[0,3] += x
            self.matrix[1,3] += y
            self.matrix[2,3] += z
        if('rotation' in kwargs):
            x, y, z = kwargs['rotation']
            self.rotate(x, y, z)
        if('scaling' in kwargs):
            x, y, z = kwargs['scaling']
            self.scale(x, y, z)

    def rotate(self, x, y, z) -> None:
        x, y, z = np.radians([x, y, z])
        rotation_z = np.matrix([[np.cos(z), -np.sin(z), 0, 0],
                                [np.sin(z), np.cos(z), 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])
        rotation_x = np.matrix([[1, 0, 0, 0],
                                [0, np.cos(x), -np.sin(x), 0],
                                [0, np.sin(x), np.cos(x), 0],
                                [0, 0, 0, 1]])
        rotation_y = np.matrix([[np.cos(y), 0, np.sin(y), 0],
                                [0, 1, 0, 0],
                                [-np.sin(y), 0, np.cos(y), 0],
                                [0, 0, 0, 1]])
        self.matrix = self.matrix.dot(rotation_z.dot(rotation_x.dot(rotation_y)))

    def scale(self, x, y, z):
        self.matrix[0,0] *= x
        self.matrix[1,1] *= y
        self.matrix[2,2] *= z

    def translate(self, x, y, z):
        self.matrix[0,3] += x
        self.matrix[1,3] += y
        self.matrix[2,3] += z