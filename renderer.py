from PIL import Image, ImageDraw
import numpy as np

def transform_matrix(op={}) -> np.array:
    result_matrix = op['matrix'] if 'matrix' in op else np.identity(4)
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
    if('scaling' in op):
        x, y, z = op['scaling']
        result_matrix[0,0] *= x
        result_matrix[1,1] *= y
        result_matrix[2,2] *= z
    return result_matrix


def render(camera : np.matrix, objects=[]):
    """ 
        Image rasterisation, convert a list of Obj instances using
        a coordinate system 
    """
    # define canvas
    img = Image.new('RGB', (500,500))
    draw = ImageDraw.Draw(img)
    # canvas virtual size (pixel size is expressed by img.size)
    w = 1
    h = w * img.size[1]/img.size[0]

    points_3d_to_2d = dict()  # keep track of drawn vertices by each object
    for obj in objects:
        # for each object convert vertices to camera CoordinateSystem and draw them
        vertices = list()
        for vertex in obj.to_camera(camera):
            # convert 3d space to canvas space
            if vertex[2] > 0:
                print("Not visible, vertex:", vertex[:3])
            if not vertex[2]:  # vertex[2] == 0 would lead to infinity in the next expression
                x = img.size[0] * vertex[0]
                y = img.size[1] * vertex[1]
            else:
                x = img.size[0] * ((vertex[0] / -vertex[2]) + w/2)/w
                y = img.size[1] * (1-((vertex[1] / -vertex[2]) + h/2)/h)
            vertices.append((x,y))
        for face in obj.faces:
            # draw faces (or wireframe)
            draw_face = list()
            visible = False
            for f in face:
                draw_face.append(vertices[f-obj.INDEX_OFFSET])
                x, y = draw_face[-1]
                if (x >= 0 and x <= img.size[0]) or (y >= 0 and y <= img.size[1]):
                    visible = True
                    print(x, y)
                else:
                    print("not visible", x, y)
            if(visible):
                if(obj.WIREFRAME):
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
        if obj.DRAW_VERTICES:
            draw.point(tuple((v[0],v[1]) for v in vertices), fill="#00FF00")  # draw vertices
        points_3d_to_2d[obj] = vertices
    img.show()
