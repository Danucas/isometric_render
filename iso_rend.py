#!/usr/bin/python3
#Isometric render in python for multiOS runnin
from read import *
from proj import *
from tkinter import *
import sys
obj = obj_read("obj/{}.txt".format(sys.argv[1]))
obj["color"] = "red"
root = Tk()
root.geometry("640x480")
project(obj, root)

root.mainloop()
