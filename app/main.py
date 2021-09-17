#!/usr/bin/python3
"""
Isometric render entrypoint
creates the tk instance window
"""

import eel
import base64
import random
from PIL import Image
import numpy as np
from utilities.linear_algebra import (
    normalize,
    nearest_intersected_object
)

eel.init('interface')
world = {
    'objects': [
        { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0, 1]), 'diffuse': np.array([0.7, 0, 0, 1]), 'specular': np.array([1, 1, 1, 1]), 'shininess': 100 },
        { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1, 1]), 'diffuse': np.array([0.7, 0, 0.7, 1]), 'specular': np.array([1, 1, 1, 1]), 'shininess': 100 },
        { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0, 1]), 'diffuse': np.array([0, 0.6, 0, 1]), 'specular': np.array([1, 1, 1, 1]), 'shininess': 100 }
    ],
    'lights': [
        { 'position': np.array([5, 5, 5]), 'ambient': np.array([1, 1, 1, 1]), 'diffuse': np.array([1, 1, 1, 1]), 'specular': np.array([1, 1, 1, 1]) }
    ]
}

@eel.expose
def open_file(filename):
    print(filename)


@eel.expose
def log(text):
    print(text)


@eel.expose
def raytrace(canvas_dimensions):
    width = canvas_dimensions.get('width')
    height = canvas_dimensions.get('height')

    ratio =  float(width) / height
    screen = (-1, 1/ratio, 1, -1/ratio)
    image = np.zeros((int(height), int(width), 4))
    image = image + np.array([0, 0, 0, 255])

    for i, y in enumerate(np.linspace(screen[1], screen[3], int(height))):
        for j, x in enumerate(np.linspace(screen[0], screen[2], int(width))):
            light = world['lights'][0]
            pixel = np.array([x, y, 0])
            origin = world['camera']
            direction = normalize(pixel - origin)

            nearest_object, min_distance = nearest_intersected_object(world['objects'], origin, direction)
            if nearest_object is None:
                continue

            intersection = origin + min_distance  * direction

            normal_to_surface = normalize(intersection - nearest_object['center'])
            shifted_point = intersection + 1e-5 * normal_to_surface

            intersection_to_light = normalize(light['position'] - shifted_point)

            _, min_distance = nearest_intersected_object(world['objects'], shifted_point, intersection_to_light)
            intersection_to_light_distance = np.linalg.norm(light['position'] - intersection)
            is_shadowed = min_distance < intersection_to_light_distance

            if is_shadowed:
                continue

            illumination = np.zeros((4))
            
            illumination += nearest_object['ambient'] * light['ambient']

            illumination += nearest_object['diffuse'] * light['diffuse'] * np.dot(intersection_to_light, normal_to_surface)

            intersection_to_camera = normalize(world['camera'] - intersection)
            H = normalize(intersection_to_light + intersection_to_camera)
            illumination += nearest_object['specular'] * light['specular'] * np.dot(normal_to_surface, H) ** (nearest_object['shininess'] / 4)

            illumination[3] = 1
            image[i, j] = np.clip(illumination, 0, 1) * 255

    pixels = np.concatenate(image).ravel().tolist()

    return pixels


def main():
    world['camera'] = np.array([0, 0, 1])
    
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
