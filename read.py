#/usr/bin/python3
"""
Read .obj .txt files an parsed to objects
"""

def obj_read(filename):
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
    for line in content:
        line = line.split(" ")
        if line[0] == "v":
            vertex.append({
                "x": float(line[1]) * scale,
                "y": float(line[2]) * scale,
                "z": float(line[3]) * scale})
        if line[0] == "f":
            del line[0]
            face = []
            for con_point in line:
                con_point = con_point.split("/")
                face.append(int(con_point[0]) - 1)
            face.append(int(line[0].split("/")[0]) - 1)
            faces.append(face)
    return ({
        "vertex": list(reversed(vertex)),
        "faces": faces})
