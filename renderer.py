from PIL import Image, ImageDraw
import numpy as np
from models import CoordinateSystem

def transform_matrix(op={}) -> np.array:
    result_matrix = op['marix'] if 'matrix' in op else np.identity(4)
    if('translation' in op):
        x, y, z = op['translation']
        result_matrix[0,3] += x
        result_matrix[1,3] += y
        result_matrix[2,3] += z
    if('rotation' in op):
        x, y, z = np.radians(op['rotation'])
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
        result_matrix = result_matrix.dot(rotation_z.dot(rotation_x.dot(rotation_y)))
    if('scale' in op):
        x, y, z = op['scale']
        result_matrix[0,0] *= x
        result_matrix[1,1] *= y
        result_matrix[2,2] *= z
    return result_matrix


def render(camera : CoordinateSystem, objects=[]):
    """ 
        Image rasterisation, convert a list of Obj instances using
        a CoordinateSystem reference 
    """
    # define canvas
    img = Image.new('RGB', (500,500))
    draw = ImageDraw.Draw(img)
    # canvas virtual size (pixel size is expressed by img.size)
    w, h = (1,1)
    # settings' values (may be implemeted in **kwargs)
    INDEX_OFFSET = 1
    WIREFRAME = 1

    points_3d_to_2d = dict()  # keep track of drawn vertices by each object
    for obj in objects:
        # for each object convert vertices to camera CoordinateSystem and draw them
        vertices = obj.to_camera(camera)
        for vertex in vertices:
            # convert 3d space to canvas space
            if vertex[2] > 0:
                print("Not visible, vertex:", vertex[:2])
            else:
                vertex[0] = img.size[0] * ((vertex[0] / -vertex[2]) + w/2)/w
                vertex[1] = img.size[1] * (1-((vertex[1] / -vertex[2]) + h/2)/h)
        for face in obj.faces:
            # draw faces (or wireframe)
            draw_face = list()
            for f in face:
                draw_face.append((vertices[f-INDEX_OFFSET][0], vertices[f-INDEX_OFFSET][1]))
            if(WIREFRAME):
                edges = list()
                for i in range(len(draw_face)):
                    # connect near vertices to an edge
                    edges.append(draw_face[i])
                    if(i == len(draw_face)-1):
                        # the last vertex must be connected to the first
                        edges.append(draw_face[0])
                    else:
                        edges.append(draw_face[i+1])
                draw.line(edges, fill="#FF0000")
            else:
                draw.polygon(draw_face, fill="#888888")
        draw.point(tuple((v[0],v[1]) for v in vertices), fill="#FF0000")  # draw vertices
        points_3d_to_2d[obj] = vertices
    img.show()
