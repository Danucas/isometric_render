#/usr/bin/python3
"""
Read .obj .txt files an parsed to objects
"""

from models.mesh import Mesh
from models.vectors import Vector3D

def read(filename):
    """
    Open file from obj folder as read
    and create vertex objects with the data
    return a dict with vertex and faces
    to render the isometric map
    """
    content = None
    scale = 1
    with open(filename, "r") as f:
        content = f.read().split("\n")
    faces = []
    vertex = []
    vertex_2 = []
    mesh = Mesh(filename.split('/')[-1].split('.')[0])
    for line in content:
        line = line.replace('  ', ' ').strip().split(" ")
        if line[0] == "v":
            vertex.append(Vector3D(
                float(line[1]) * scale,
                float(line[2]) * scale,
                float(line[3]) * scale
            ))
        if line[0] == "f":
            del line[0]
            face = []
            for con_point in line:
                con_point = con_point.split("/")

                face.append(int(con_point[0]) - 1)
            # face.append(int(line[0].split("/")[0]) - 1)
            faces.append(face)
    mesh.vertices = vertex
    mesh.faces = faces
    mesh.calculate_center()
    return mesh
