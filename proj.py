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
        w1 = dim["width"]
        h1 = dim["height"]
        x1 = proj_vert(vr[len(vr) - 1 - pos], w1, h1)["x"]
        x2 = proj_vert(vr[pos], dim["width"], dim["height"])["x"]
        y1 = proj_vert(vr[0], w1, h1)["y"]
        y2 = proj_vert(vr[len(vr) - 1], w1, h1)["y"]
        w = x1 - x2
        h = y1 - y2
        return w, h

def project_vertexs(obj, viewport, scx, scy):
    w = viewport["width"]
    h = viewport["height"]
    projected = []
    for vertex in obj["vertex"]:
        projected.append(proj_vert(vertex, w * scx, h * scy))
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

    tr_w, tr_h = get_iso_map_width(obj, dim)
    scr_reg_w = int((tr_w / dim["width"])) + 2
    scr_reg_h = int((tr_h / dim["height"])) + 2
    pvs = project_vertexs(obj, dim, scr_reg_w, scr_reg_h)
    print("scrolling region", dim["width"] * scr_reg_w, dim["height"] * scr_reg_h)
    canvas = Canvas(root, width=dim["width"], height=dim["height"], scrollregion=[0, 0, dim["width"] * scr_reg_w, dim["height"] * (scr_reg_h)])
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

    def getTileSize(can):
        box = can.bbox(1)
        w = box[2] - box[0]
        h = box[3] - box[1]
        print("Tile size: ", w, h)
        return (w, h)

    tile_size = getTileSize(canvas)
    scroll_view = scroll_zoom(canvas)
    cnv[0] = canvas
    return tile_size
    # print(projected_vertx)
