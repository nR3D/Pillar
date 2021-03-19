from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from pillar.transformation import Transformation

class Renderer():
    def __init__(self, camera : np.matrix, objs = [], **kwargs):
        self.camera = camera
        self.objs = objs
        self.WIREFRAME = kwargs.get('WIREFRAME', False)
        self.SOLID = kwargs.get('SOLID', True)
        self.VERTICES = kwargs.get('VERTICES', False)
        self.INDEX_OFFSET = kwargs.get('INDEX_OFFSET', 1)
        self.__image = None
    
    def __render_vertices(self, vertices : list, color="#00FF00"):
        ImageDraw.Draw(self.__image).point(tuple((v[0],v[1]) for v in vertices), fill=color)  # draw vertices

    def __render_wireframe(self, faces : list, color="#FF0000"): 
        edges = list()
        for i in range(len(faces)):
            # connect near vertices to an edge
            edges.append(faces[i])
            if(i == len(faces)-1):
                # the last vertex must be connected to the first
                edges.append(faces[0])
            else:
                edges.append(faces[i+1])
        ImageDraw.Draw(self.__image).line(edges, fill=color)

    def __render_solid_face(self, faces : list, color="#888888"): 
        ImageDraw.Draw(self.__image).polygon(faces, fill=color)
    
    def render(self):
        # define canvas
        self.__image = Image.new('RGBA', (500,500), (0,0,0,0))
        # canvas virtual size (pixel size is expressed by img.size)
        w = 1
        h = w * self.__image.size[1]/self.__image.size[0]
        
        vertices = list()
        z_depth = list()
        faces = list()
        for obj in self.objs:
            # copy faces adjusting the index value for each object
            previous_len = len(vertices)
            for face in obj.faces:
                faces.append([f+previous_len for f in face])
            # for each object convert vertices to camera CoordinateSystem and draw them
            for vertex in obj.iter_vertices(self.camera.matrix):
                # convert 3d space to canvas space
                if vertex[2] > 0:  # debug print
                    print("Not visible, vertex:", vertex[:3])
                if not vertex[2]:  # vertex[2] == 0 would lead to division by zero in the next expression
                    x = self.__image.size[0] * vertex[0]
                    y = self.__image.size[1] * vertex[1]
                else:
                    x = self.__image.size[0] * ((vertex[0] / -vertex[2]) + w/2)/w
                    y = self.__image.size[1] * (1-((vertex[1] / -vertex[2]) + h/2)/h)
                vertices.append((x,y))
                z_depth.append(vertex[2])
        
        depth_faces = list()
        for face in faces:
            if not len(depth_faces):
                depth_faces.append(face)
            else:
                for i in range(len(depth_faces)):  # raw z-depth implementation (doesn't work for crossing faces)
                    if sum([z_depth[f-self.INDEX_OFFSET] for f in face])/len(face) < sum(
                            z_depth[f-self.INDEX_OFFSET] for f in depth_faces[i])/len(depth_faces[i]):
                        depth_faces.insert(i, face)
                        break
                    elif i == len(depth_faces) - 1:
                        depth_faces.append(face)
        
        for face in depth_faces:
            # draw faces (or wireframe)
            draw_face = list()
            visible = False
            for f in face:
                draw_face.append(vertices[f-self.INDEX_OFFSET])
                x, y = draw_face[-1]
                if (x >= 0 and x <= self.__image.size[0]) or (y >= 0 and y <= self.__image.size[1]):
                    visible = True
            if visible:
                if self.SOLID:
                    z_face = [z_depth[f-self.INDEX_OFFSET] for f in face]
                    color = self.blend_color(obj.color, '#000000', float(sum(z_face)/(len(face)*min(z_depth))))
                    self.__render_solid_face(draw_face, color)
                if self.WIREFRAME:
                    self.__render_wireframe(draw_face)
                if self.VERTICES:
                    self.__render_vertices([vertices[f-self.INDEX_OFFSET],])
        self.__image.show()

    @staticmethod
    def blend_color(color1 : str, color2 : str, scale=0.5) -> str:
        """
            Blend two colors in a scale between 0 and 1
            e.g color1 = '#000000', color2 = '#FFFFFF', scale = 0.5 (i.e. 50%)
            scale=0 returns color1, scale=1 returns color2
        """
        if color1[0] != '#' or color2[0] != '#':
            assert "Colors must be a string of hex values"
        if scale > 1:
            scale = 1
        elif scale < 0:
            scale = 0
        
        result = '#'
        R = hex(round((int(color2[1:3], 16) - int(color1[1:3], 16))*scale + int(color1[1:3], 16)))[2:]
        G = hex(round((int(color2[3:5], 16) - int(color1[3:5], 16))*scale + int(color1[3:5], 16)))[2:]
        B = hex(round((int(color2[5:7], 16) - int(color1[5:7], 16))*scale + int(color1[5:7], 16)))[2:]
        result += R if len(R) == 2 else '0'+R
        result += G if len(G) == 2 else '0'+G
        result += B if len(B) == 2 else '0'+B
        return result
