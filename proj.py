#!/usr/bin/python3
from tkinter import *

def proj_vert(vertex, w, h):
    inc = 0.7
    x, y, z = float(vertex["x"]), float(vertex["y"]), float(vertex["z"])
    Px = (inc * x) - (inc * y) + (w / 2)
    Py = ((1 - inc) * x) + ((1 - inc) * y) - z + (h / 2)
    return {"x": int(Px), "y": int(Py)}

def get_iso_map_width(terrain, dim):
    if "faces" in terrain and "vertex" in terrain:
        fs = terrain["faces"]
        vr = terrain["vertex"]
        pos = fs[0][3] - 1
        w = proj_vert(vr[len(vr) - 1 - pos], dim["width"], dim["height"])["x"] - proj_vert(vr[pos], dim["width"], dim["height"])["x"]
        return w

def project_vertexs(obj, viewport, scr_reg):
    w = viewport["width"]
    h = viewport["height"]
    projected = []
    for vertex in obj["vertex"]:
        projected.append(proj_vert(vertex, w * scr_reg, h * scr_reg))
    return projected
def scroll_zoom(canvas):
    scl_cont = Canvas(canvas, width=20, height=210, bg="white", cursor="hand2")
    scl_cont.create_rectangle(7, 4, 13, 206, fill="grey")
    selector = scl_cont.create_oval(2, 2, 19, 20, fill="white")
    last = [0]
    clkd = [False]
    def motion(evn):
        if clkd[0] is True:
            pos = evn.y - 9
            if evn.y > 9 and evn.y < 201:
                diff = int(pos) -last[0]
                scl_cont.move(selector, 0, diff)
                last[0] = pos
    def released(evn):
        clkd[0] = False

    def clicked(evn):
        clkd[0] = True
    scl_cont.bind("<Button-1>", clicked)
    scl_cont.bind("<Motion>", motion)
    scl_cont.bind("<ButtonRelease-1>", released)
    scl_cont.place(x=4, y=20)

def terrain_grid(obj, root, cnv):
    #Projected vertices
    dim = {"width": root.winfo_screenwidth(), "height": root.winfo_screenheight()}

    tr_w = get_iso_map_width(obj, dim)
    scr_reg = int((tr_w / dim["width"])) + 2
    pvs = project_vertexs(obj, dim, scr_reg)
    print("scrolling region", scr_reg)
    canvas = Canvas(root, width=dim["width"], height=dim["height"], scrollregion=[0, 0, dim["width"] * scr_reg, dim["height"] * (scr_reg)])
    canvas.place(x=0, y=0)
    canvas.xview_moveto(0.5)
    canvas.yview_moveto(0.5)
    bbcan = [None]
    act_tile = [None]
    clicked  = [None]
    def color_tile(evn, color):
        #print("Over coord: ", evn.x , evn.y)
        item = canvas.find_closest(canvas.canvasx(evn.x), canvas.canvasy(evn.y), halo=None, start=None)
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
        item = canvas.find_closest(canvas.canvasx(evn.x), canvas.canvasy(evn.y), halo=None, start=None)
        bbox = canvas.bbox(item[0])
        #print("tile width is {}".format(bbox[2] - bbox[0]))
        canvas.itemconfigure(item[0], fill="#cffc03")
        clicked[0] = item[0]
        print(item[0], pvs[item[0] - 1])
        print("x, y view: ", canvas.canvasx(evn.x), canvas.canvasy(evn.y))
        #print(dir(canvas))

    #Drawing each polygon
    for f in obj["faces"]:
        poly = []
        for el in f:
            if el < len(pvs) and el > -1:
                poly.append(pvs[el]["x"])
                poly.append(pvs[el]["y"])
        canvas.create_polygon(poly, fill=obj["color"], outline="black")
    canvas.bind("<Motion>", lambda evn: tile_mot(evn))
    canvas.bind("<Button-1>", lambda evn: tile_click(evn))
    scroll_view = scroll_zoom(canvas)
    cnv[0] = canvas
    # print(projected_vertx)
