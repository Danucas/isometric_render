#!/usr/bin/python3
from tkinter import *
def project_vertexs(obj, viewport):
    inc = 0.7
    width = viewport["width"]
    height = viewport["height"]
    projected = []
    for vertex in obj["vertex"]:
        x, y, z = float(vertex["x"]), float(vertex["y"]), float(vertex["z"])
        Px = (inc * x) - (inc * y) + (width / 2)
        Py = ((1 - inc) * x) + ((1 - inc) * y) - z + (height / 2)
        projected.append({"x": int(Px), "y": int(Py)})
    return projected

def project(obj, root):
    #Projected vertices
    pvs = project_vertexs(obj, {"width": 640, "height": 480})
    canvas = Canvas(root, width=640, height=480)
    canvas.place(x=0, y=0)
    bbcan = [None]
    act_tile = [None]
    clicked  = [None]
    def color_tile(evn, color):
        item = canvas.find_closest(evn.x, evn.y, halo=None, start=None)
        if act_tile[0] is not None and item[0] is not None:
            canvas.config(cursor="hand2")
            if act_tile[0] != item[0]:
                canvas.config
                canvas.itemconfigure(act_tile[0], fill="red")
                clicked[0] = False
            else:
                if clicked[0] is not None and clicked[0] != act_tile[0]:
                    canvas.itemconfigure(item[0], fill=color)
        elif item[0] is None:
            canvas.config(cursor="")
        act_tile[0] = item[0]

    def tile_mot(evn):
        color_tile(evn, "blue")

    def tile_click(evn):
        item = canvas.find_closest(evn.x, evn.y, halo=None, start=None)
        canvas.itemconfigure(item[0], fill="#cffc03")
        clicked[0] = item[0]
        print(item[0], pvs[item[0] - 1])

    #Drawing each polygon
    for f in obj["faces"]:
        poly = []
        for el in f:
            poly.append(pvs[el]["x"])
            poly.append(pvs[el]["y"])
        canvas.create_polygon(poly, fill=obj["color"], outline="black")
    canvas.bind("<Motion>", lambda evn: tile_mot(evn))
    canvas.bind("<Button-1>", lambda evn: tile_click(evn))
    # print(projected_vertx)
