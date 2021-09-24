from models.base import BaseModel
import math
import numpy as np

class Mesh(BaseModel):
    name = None
    faces = None
    vertices = None
    color = None
    center = None


    def __init__(self, name='Mesh', *args, **kwargs):
        super().__init__(asset_type='Mesh', *args, **kwargs)
        self.translation = np.array([0, 0, 0])
        self.name = name

    
    def scale(self, vertices, scalar=None):
        if scalar is None:
            scalar = self.scalar
        return ([
            self.scale_vertex(vertice)
            for vertice in vertices
        ])


    def scale_vertex(self, vertex):
        center = self.center
        distance = vertex - center

        print('distance: ', distance)
        print('vertex final position: ', vertex + (distance * self.scalar))
        return vertex + (distance * self.scalar)


    def translate(self, vertices, translation=None):
        if translation is None:
            translation = self.translation
        return ([
            np.array(
                [
                    vertice[0] + translation[0],
                    vertice[1] + translation[1],
                    vertice[2] + translation[2]
                ]
            )
            for vertice in vertices
        ])
    

    def rotate(self, vertices, rotation=None):
        rotated_vertices = []
        if rotation is None:
            rotation = self.rotation
        for ver in vertices:
            tempx = ver[0]
            tempy = ver[1]
            tempz = ver[2]
            overX = rotation[0]
            overY = rotation[1]
            overZ = rotation[2]
            # Rotar en X
            i = (1)*(tempx)+(0)*(tempy)+(0)*(tempz)
            j = (0)*(tempx)+(math.cos(overX))*(tempy)+(-(math.sin(overX)))*(tempz)
            k = (0)*(tempx)+(math.sin(overX))*(tempy)+(math.cos(overX))*(tempz)
            tempx = i
            tempy = j
            tempz = k
            # Rotar en Y
            i = (math.cos(overY))*(tempx)+(0)*(tempy)+(math.sin(overY))*(tempz)
            k = (-(math.sin(overY)))*(tempx)+(0)*(tempy)+(math.cos(overY))*(tempz)
            j = (0)*(tempx)+(1)*(tempy)+(0)*(tempz)
    
            tempx = i
            tempy = j
            tempz = k
    
            # Rotar en z
    
            i = (math.cos(overZ))*(tempx)+(-(math.sin(overZ)))*(tempy)+(0)*(tempz)
            j = (math.sin(overZ))*(tempx)+(math.cos(overZ))*(tempy)+(0)*(tempz)
            k = (0)*(tempx)+(0)*(tempy)+(1)*(tempz)
    
            x = i
            y = j
            z = k
  
            rotated_vertices.append(np.array(
                [x, y, z]
            ))
        return rotated_vertices


    def normalize(self, vertices, dimensions):
        return [
            np.array(
                [
                    int(vertice[0] + (dimensions.get('width')/4)),
                    int((dimensions.get('height') / 2) - (vertice[1] + (dimensions.get('height')/4))),
                    vertice[2]
                ]
            )
            for vertice in vertices
        ]


    def calculate_center(self, vertices=None):
        should_return = False
        if vertices is None:
            vertices = self.vertices
        else:
            should_return = True
        xAvg = sorted(vertices, key=lambda v: v[0], reverse=True)
        yAvg = sorted(vertices, key=lambda v: v[1], reverse=True)
        zAvg = sorted(vertices, key=lambda v: v[2], reverse=True)
        center = np.array(
            [
                xAvg[-1][0] + ((xAvg[0][0] - xAvg[-1][0]) / 2),
                yAvg[-1][1] + ((yAvg[0][1] - yAvg[-1][1]) / 2),
                zAvg[-1][2] + ((zAvg[0][2] - zAvg[-1][2]) / 2),
            ]
        )
        if should_return:
            return center
        else:
            self.center = center

    def clip(self, pov, faces):
        sorted_faces = sorted(faces, key=lambda f: self.calculate_center(f)[2] - pov[2])
        print('clipped_faces: ')
        clipped_faces = []
        for face in sorted_faces:
            center = self.calculate_center(face)
            distance = center[2] - pov[2]
            if distance > 0:
                clipped_faces.append(face)
            print('pov: ', pov)
            print('face pos: ', face)
            print('distance: ', distance)
            print('center', center)

        return list(reversed(clipped_faces))
        # return clipped_faces


    def __str__(self):
        return """{}
        name: {}
        center: {} 
        position: {}
        """.format(self.id, self.name, self.center, self.position)