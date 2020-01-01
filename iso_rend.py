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
pad_x = 300
pad_y = 200
root.geometry("{}x{}+0+0".format(root.winfo_screenwidth() - pad_x, root.winfo_screenheight() - pad_y))

def keydown(evn):
       print(evn.char)
       x, y = 0.0031, 0.0021
       #Testing key events
       if evn.char == "a":
              if cam[0]["tr"]["x"] > 0.01 and cam[0]["tr"]["y"] < 1:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] - x
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] - y

       elif evn.char == "d":
              if cam[0]["tr"]["x"] < 1 and cam[0]["tr"]["y"] < 1:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] + x
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] + y

       elif evn.char == "w":
              if cam[0]["tr"]["y"] > 0.01 and cam[0]["tr"]["x"] > 0.01:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] + x
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] - y

       elif evn.char == "s":
              if cam[0]["tr"]["y"] < 1 and cam[0]["tr"]["x"] > 0.01:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] - x
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] + y

       #normal navigation
       elif evn.char == "z":
              if cam[0]["tr"]["x"] > 0.01:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] - 0.01
       elif evn.char == "v":
              if cam[0]["tr"]["x"] < 1:
                     cam[0]["tr"]["x"] = cam[0]["tr"]["x"] + 0.01
       elif evn.char == "c":
              if cam[0]["tr"]["y"] > 0.01:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] - 0.01
       elif evn.char == "x":
              if cam[0]["tr"]["y"] < 1:
                     cam[0]["tr"]["y"] = cam[0]["tr"]["y"] + 0.01

       #Aplying changes to canvas
       canvas[0].xview_moveto(cam[0]["tr"]["x"])
       canvas[0].yview_moveto(cam[0]["tr"]["y"])
       print("{:.2f} {:.2f}".format(cam[0]["tr"]["x"], cam[0]["tr"]["y"]))


terrain_width = get_iso_map_width(terrain, {"width": root.winfo_screenwidth(), "height": root.winfo_screenheight()})

print("terrain width: ", terrain_width)

terrain_grid(terrain, root, canvas)
#print(dir(canvas[0]))
root.bind("<KeyPress>", lambda evn: keydown(evn))


root.mainloop()
