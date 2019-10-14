from PIL import Image, ImageDraw
import numpy as np

def transform_matrix(**kwargs) -> np.matrix:
    result_matrix = kwargs.get('matrix', np.identity(4))
    if('translation' in kwargs):
        x, y, z = kwargs['translation']
        result_matrix[0,3] += x
        result_matrix[1,3] += y
        result_matrix[2,3] += z
    if('rotation' in kwargs):
        x, y, z = np.radians(kwargs['rotation'])
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
    if('scaling' in kwargs):
        x, y, z = kwargs['scaling']
        result_matrix[0,0] *= x
        result_matrix[1,1] *= y
        result_matrix[2,2] *= z
    return np.matrix(result_matrix)

def render_vertices(vertices : list, img : Image.Image, color="#00FF00"):
    draw = ImageDraw.Draw(img)
    draw.point(tuple((v[0],v[1]) for v in vertices), fill=color)  # draw vertices

def render_wireframe(faces : list, img : Image.Image, color="#FF0000"): 
    draw = ImageDraw.Draw(img)
    edges = list()
    for i in range(len(faces)):
        # connect near vertices to an edge
        edges.append(faces[i])
        if(i == len(faces)-1):
            # the last vertex must be connected to the first
            edges.append(faces[0])
        else:
            edges.append(faces[i+1])
    draw.line(edges, fill=color)

def render_solid_face(faces : list, img : Image.Image, color="#888888"): 
    draw = ImageDraw.Draw(img)
    draw.polygon(faces, fill=color)

def render(camera : np.matrix, objects=[], **kwargs):
    """ 
        Image rasterisation, convert a list of Obj instances using
        a coordinate system 
    """
    # define canvas
    img = Image.new('RGB', (500,500))
    # canvas virtual size (pixel size is expressed by img.size)
    w = 1
    h = w * img.size[1]/img.size[0]

    points_3d_to_2d = dict()  # keep track of drawn vertices by each object
    for obj in objects:
        # for each object convert vertices to camera CoordinateSystem and draw them
        vertices = list()
        for vertex in obj.iter_vertices(camera):
            # convert 3d space to canvas space
            if vertex[2] > 0:
                print("Not visible, vertex:", vertex[:3])
            if not vertex[2]:  # vertex[2] == 0 would lead to division by zero in the next expression
                x = img.size[0] * vertex[0]
                y = img.size[1] * vertex[1]
            else:
                x = img.size[0] * ((vertex[0] / -vertex[2]) + w/2)/w
                y = img.size[1] * (1-((vertex[1] / -vertex[2]) + h/2)/h)
            vertices.append((x,y))
        depth_faces = list()
        for face in obj.faces:
            if not len(depth_faces):
                depth_faces.append(face)
            else:
                for i in range(len(depth_faces)):  # raw z-depth implementation (doesn't work for crossing faces)
                    if sum([obj.vertices[f-obj.INDEX_OFFSET][2] for f in face])/len(face) < sum(
                            obj.vertices[f-obj.INDEX_OFFSET][2] for f in depth_faces[i])/len(depth_faces[i]):
                        depth_faces.insert(i, face)
                        break
                    elif i == len(depth_faces) - 1:
                        depth_faces.append(face)
        for face in depth_faces:
            # draw faces (or wireframe)
            draw_face = list()
            visible = False
            for f in face:
                draw_face.append(vertices[f-obj.INDEX_OFFSET])
                x, y = draw_face[-1]
                if (x >= 0 and x <= img.size[0]) or (y >= 0 and y <= img.size[1]):
                    visible = True
            if visible:
                if kwargs['WIREFRAME'] if 'WIREFRAME' in kwargs else obj.WIREFRAME:
                    render_wireframe(draw_face, img)
                else:
                    render_solid_face(draw_face, img)
        if kwargs['DRAW_VERTICES'] if 'DRAW_VERTICES' in kwargs else obj.DRAW_VERTICES:
            render_vertices(vertices, img)
        points_3d_to_2d[obj] = vertices
    img.show()

