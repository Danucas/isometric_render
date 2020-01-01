#!/usr/bin/python3
import sys
f = open("plane", "w")
length = int(sys.argv[1])
for x in range(length):
    for y in range(length):
        sep = ""
        if y == length - 1 and x < length - 1:
            sep = "\n"
        elif x < length and y < length - 1:
            sep = " "
        f.write("0{}".format(sep))
f.close()
