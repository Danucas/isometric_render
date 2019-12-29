#!/usr/bin/python3
import sys
f = open(sys.argv[1], "r")
content = f.read()
lines = content.split("\n")
faces = []
for y, line in enumerate((lines)):
    if len(line) > 1:
        for x, z in enumerate((line.split(" "))):
            anch = len(line.split(" "))
            z = int(z)
            #       z = 0
            dis = 180
            print("v {} {} {}".format((x - (anch / 2)) * dis, (y - (anch / 2)) * dis, z))
            if (y < len(lines) - 1) and (x < anch - 1):
                faces.append("{}/{} {}/{} {}/{} {}/{}".format((y * anch) + x + 1,
                                                              (y * anch) + x + 2,
                                                              (y * anch) + x + 2,
                                                              ((y + 1) * anch) + x + 2,
                                                              ((y + 1) * anch) + x + 2,
                                                              ((y + 1) * anch) + x + 1,
                                                              ((y + 1) * anch) + x + 1,
                                                              (y * anch) + x + 1))

for i, face in enumerate(faces):
    print("f {}".format(face))
