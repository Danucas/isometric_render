#!/usr/bin/python3
#Isometric render in python for multiOS running
from read import *
from proj import *
from tkinter import *
import sys
terrain = obj_read("obj/{}.txt".format(sys.argv[1]))
terrain["color"] = "red"
cam = [{"tr": {"x": 0.5,"y": 0.5}}]
canvas = [None]
root = Tk()
pad_x = 0
pad_y = 0
w = 720  #root.winfo_screenwidth()
h = 640  #root.winfo_screenheight()
root.geometry("{}x{}+0+0".format(w, h))

def keydown(evn, tlen):
       #Show the pressed key
       print(evn.char)

       # set the width and height to be meassured
       reg = canvas[0].cget("scrollregion")
       reg = reg.split(" ")
       w , h = float(reg[2]), float(reg[3])
       w = w #- root.winfo_screenwidth()
       h = h #- root.winfo_screenheight()
       tw = float("{:f}".format((tlen[0] / 2) / w))
       th = float("{:f}".format((tlen[1] / 2) / h))

       #x, y = 0.0031, 0.0021
       x, y = tw , th
       print("===============================")
       print("region: ", w, h, "position: ", x, y, "steps percent: ", tw, th)
       print("===============================")
       #Testing key events
       if evn.char == "a":
              if cam[0]["tr"]["x"] > 0.01:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] - x
              if cam[0]["tr"]["y"] < 1:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] - y

       elif evn.char == "d":
              if cam[0]["tr"]["x"] < 1:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] + x
              if cam[0]["tr"]["y"] < 1:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] + y

       elif evn.char == "w":
              if cam[0]["tr"]["y"] > 0.01:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] + x
              if cam[0]["tr"]["x"] > 0.01:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] - y

       elif evn.char == "s":
              if cam[0]["tr"]["y"] < 1:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] - x
              if cam[0]["tr"]["x"] > 0.01:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] + y

       #normal navigation
       elif evn.char == "z":
              if cam[0]["tr"]["x"] > 0.01:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] - x
       elif evn.char == "v":
              if cam[0]["tr"]["x"] < 1:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] + x
       elif evn.char == "c":
              if cam[0]["tr"]["y"] > 0.01:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] - y
       elif evn.char == "x":
              if cam[0]["tr"]["y"] < 1:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] + y

       #Aplying changes to canvas
       canvas[0].xview_moveto(cam[0]["tr"]["x"])
       canvas[0].yview_moveto(cam[0]["tr"]["y"])
       print("{:.2f} {:.2f}".format(cam[0]["tr"]["x"], cam[0]["tr"]["y"]))


terrain_width = get_iso_map_width(terrain, {"width": root.winfo_screenwidth(), "height": root.winfo_screenheight()})

print("terrain width: ", terrain_width)

tile_w, tile_h = terrain_grid(terrain, root, canvas)
#print(dir(canvas[0]))
root.bind("<KeyPress>", lambda evn: keydown(evn, (tile_w, tile_h)))


root.mainloop()
