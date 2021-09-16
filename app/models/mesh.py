from models.base import BaseModel
from models.vectors import Vector3D
import math

class Mesh(BaseModel):
    name = None
    faces = None
    vertices = None
    color = None
    center = None

    def __init__(self, name='Mesh', *args, **kwargs):
        super().__init__(asset_type='Mesh', *args, **kwargs)
        self.translation = Vector3D(0, 0, 0)
        self.name = name


    def translate(self, vertices, translation=None):
        if translation is None:
            translation = self.translation
        return ([
            Vector3D(
                vertice.x + translation.x,
                vertice.y + translation.y,
                vertice.z + translation.z
            )
            for vertice in vertices
        ])
    

    def rotate(self, vertices, rotation=None):
        rotated_vertices = []
        if rotation is None:
            rotation = self.rotation
        for ver in vertices:
            tempx = ver.x
            tempy = ver.y
            tempz = ver.z
            overX = rotation.x
            overY = rotation.y
            overZ = rotation.z
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
  
            rotated_vertices.append(Vector3D(
                x, y, z
            ))
        return rotated_vertices

    def normalize(self, vertices, dimensions):
        return [
            Vector3D(
                int(vertice.x + dimensions.get('width') / 4),
                int(vertice.y + dimensions.get('height') / 4),
                vertice.z
            )
            for vertice in vertices
        ]

    def calculate_center(self):
        xAvg = sorted(self.vertices, key=lambda v: v.x, reverse=True)
        yAvg = sorted(self.vertices, key=lambda v: v.y, reverse=True)
        zAvg = sorted(self.vertices, key=lambda v: v.z, reverse=True)
        print(type(xAvg))
        self.center = Vector3D(
            int((xAvg[-1].x - xAvg[0].x) / 2),
            int((yAvg[-1].y - xAvg[0].y) / 2),
            int((zAvg[-1].z - xAvg[0].z) / 2),
        )

    def __str__(self):
        return """{}
        name: {}
        center: {} 
        position: {}         mk,lñdlhyer4
        """.format(self.id, self.name, self.center, self.position)