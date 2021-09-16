#!/usr/bin/python3
"""
Isometric render entrypoint
creates the tk instance window
"""

import eel

@eel.expose
def open_file(filename):
    print(filename)


def main():
    eel.init('interface')
    eel.start('index.html')

if __name__ == '__main__':
    main()






# OBJ_DIR = 'obj'


# # TODO: Primitive cam object -> implement Camera Intances from proj/
# cam = [{"tr": {"x": 0.5,"y": 0.5}}]
# step = 10
# rotation_avg = 0.2

# # Create the main APP Window
# root = Tk()
# pad_x = 0
# pad_y = 0
# w = root.winfo_screenwidth()
# h = root.winfo_screenheight()
# root.geometry("{}x{}+0+0".format(w, h))


# # TODO: keydown must be implemented on the Engine class
# # Needs to choose between UI_layers and create Interfaces to different uses
# def keydown(evn, tlen):
#     """
#     detects pressed keys to move the view
#     """
#     reg = engine.canvas.cget("scrollregion")
#     reg = reg.split(" ")
#     w , h = float(reg[2]), float(reg[3])
#     w = w
#     h = h
#     tw = float("{:f}".format((tlen[0] / 2) / w))
#     th = float("{:f}".format((tlen[1] / 2) / h))
#     #x, y = 0.0031, 0.0021
#     x, y = tw , th
#     # Mesh Controls 
#     if evn.char == "a":
#         mesh.translation = Vector3D(
#             mesh.translation.x - step,
#             mesh.translation.y,
#             mesh.translation.z
#         )
#     elif evn.char == "d":
#         mesh.translation = Vector3D(
#             mesh.translation.x + step,
#             mesh.translation.y,
#             mesh.translation.z
#         )
#     elif evn.char == "w":
#         mesh.translation = Vector3D(
#             mesh.translation.x,
#             mesh.translation.y + step,
#             mesh.translation.z
#         )
#     elif evn.char == "s":
#         mesh.translation = Vector3D(
#             mesh.translation.x,
#             mesh.translation.y - step,
#             mesh.translation.z
#         )
#     elif evn.char == "e":
#         mesh.translation = Vector3D(
#             mesh.translation.x,
#             mesh.translation.y,
#             mesh.translation.z - step
#         )
#     elif evn.char == "r":
#         mesh.translation = Vector3D(
#             mesh.translation.x,
#             mesh.translation.y,
#             mesh.translation.z + step
#         )
#     elif evn.char == "z":
#         mesh.rotation = Vector3D(
#             mesh.rotation.x + rotation_avg,
#             mesh.rotation.y,
#             mesh.rotation.z,
#         )
#     # elif evn.char == "v":
#     #     mesh.rotation = Vector3D(
#     #         mesh.rotation.x - rotation_avg,
#     #         mesh.rotation.y,
#     #         mesh.rotation.z,
#     #     )
#     elif evn.char == "c":
#         mesh.rotation = Vector3D(
#             mesh.rotation.x,
#             mesh.rotation.y + rotation_avg,
#             mesh.rotation.z,
#         )
#     elif evn.char == "x":
#         mesh.rotation = Vector3D(
#             mesh.rotation.x,
#             mesh.rotation.y - rotation_avg,
#             mesh.rotation.z,
#         )
#     # Camera Controls
#     elif evn.char == "j":
#         camera.rotation = Vector3D(
#             camera.rotation.x,
#             camera.rotation.y - rotation_avg,
#             camera.rotation.z,
#         )
#     elif evn.char == "i":
#         camera.rotation = Vector3D(
#             camera.rotation.x,
#             camera.rotation.y + rotation_avg,
#             camera.rotation.z,
#         )
#     elif evn.char == "h":
#         camera.rotation = Vector3D(
#             camera.rotation.x - rotation_avg,
#             camera.rotation.y,
#             camera.rotation.z,
#         )
#     elif evn.char == "u":
#         camera.rotation = Vector3D(
#             camera.rotation.x + rotation_avg,
#             camera.rotation.y,
#             camera.rotation.z,
#         )
#     elif evn.char == "k":
#         camera.rotation = Vector3D(
#             camera.rotation.x,
#             camera.rotation.y,
#             camera.rotation.z - rotation_avg,
#         )
#     elif evn.char == "o":
#         camera.rotation = Vector3D(
#             camera.rotation.x,
#             camera.rotation.y,
#             camera.rotation.z + rotation_avg,
#         )
#     elif evn.char == "v":
#         camera.translation = Vector3D(
#             camera.translation.x - step,
#             camera.translation.y,
#             camera.translation.z,
#         )
#     elif evn.char == "b":
#         camera.translation = Vector3D(
#             camera.translation.x + step,
#             camera.translation.y,
#             camera.translation.z,
#         )
#     elif evn.char == 'n':
#         camera.translation = Vector3D(
#             camera.translation.x,
#             camera.translation.y - step,
#             camera.translation.z,
#         )
#     elif evn.char == 'm':
#         camera.translation = Vector3D(
#             camera.translation.x,
#             camera.translation.y + step,
#             camera.translation.z,
#         )
#     elif evn.char == 'l':
#         camera.translation = Vector3D(
#             camera.translation.x,
#             camera.translation.y,
#             camera.translation.z - (step * 2),
#         )
#     elif evn.char == 'p':
#         camera.translation = Vector3D(
#             camera.translation.x,
#             camera.translation.y,
#             camera.translation.z + (step * 2),
#         )
#     engine.render()
#     print(camera, mesh)

# # Create the objects to render using obj_read
# mesh = obj.read("{}/plane.obj".format(OBJ_DIR))
# mesh.color = 'red'

# tree = obj.read("{}/lowpolytree.obj".format(OBJ_DIR))
# tree.color = 'green'
# tree.translation = Vector3D(0, 0, 200)
# # ----------------

# # Create the camera
# camera = Camera(Vector3D(0, 0, 0))

# # Create the Engine, add camera and setup the scroll and view region
# # for 'perspective' projection_type
# engine = Engine3D(root, projection_type='perspective', mode='Test')
# engine.add_camera(camera)
# engine.setup(mesh)

# # Add the objects to the engine
# engine.add_object(mesh)
# engine.add_object(tree)

# # Call render to create the key binders
# tile_w, tile_h = engine.render()

# def key_binder(evn):
#     return keydown(evn, (tile_w, tile_h))

# # Binds the key listener
# root.bind("<KeyPress>", key_binder)
# print(engine)
# root.mainloop()
