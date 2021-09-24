#!/Users/daniel/.pyenv/versions/3.5.7/bin/python3
"""
Isometric render entrypoint
creates the tk instance window
"""

import eel
import math
import base64
import sys
import random
from PIL import Image
import numpy as np
from utilities.linear_algebra import (
    normalize,
    nearest_intersected_object
)
from engine.engine import Engine3D
from models.cameras import Camera
import utilities.obj as obj

OBJ_DIR = '../resources'
DEBUG = True if len(sys.argv) > 1 and (sys.argv[1] == '--debug' or sys.argv[1] == '-d') else False

engine3d = None

eel.init('interface')

## Migrate to the existing classes
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
##


@eel.expose
def open_file(filename):
    print(filename)


@eel.expose
def log(text):
    print(text)


@eel.expose
def key_pressed(key):
    print(key)
    # Define a router for this keys pressed
    if key == 'a':
        engine3d.cameras[0].translation = engine3d.cameras[0].translation + np.array([
            -4, 0, 0
        ])
    if key == 'd':
        engine3d.cameras[0].translation = engine3d.cameras[0].translation + np.array([
            4, 0, 0
        ])
    if key == 'w':
        engine3d.cameras[0].translation = engine3d.cameras[0].translation + np.array([
            0, 4, 0
        ])
    if key == 's':
        engine3d.cameras[0].translation = engine3d.cameras[0].translation + np.array([
            0, -4, 0
        ])


@eel.expose
def raytrace(canvas_dimensions):
    return engine3d.raytrace(canvas_dimensions)


@eel.expose
def ortho(canvas_dimensions):
    return engine3d.wireframe('ortho', canvas_dimensions)


@eel.expose
def perspective(canvas_dimensions):
    return engine3d.wireframe('perspective', canvas_dimensions)


def main():
    global engine3d
    world['camera'] = np.array([0, 0, 1])
    

    # Create the objects to render using obj_read
    mesh = obj.read("{}/cube.obj".format(OBJ_DIR))
    mesh.color = 'red'
    mesh.translation = np.array([0, 0, 0])
    mesh.scalar = 40
    mesh.rotation = np.array([6, math.pi * 1.75, 0])
    # Create the camera
    camera = Camera(np.array([0, 0, 0]))
    camera.translation = np.array([0, 0, -200])
    # camera.rotation = np.array([0, 0, math.pi])

    # Create the Engine, add camera and setup the scroll and view region
    # # for 'perspective' projection_type
    engine3d = Engine3D(projection_type='perspective', mode='Test')
    engine3d.add_camera(camera)
    engine3d.add_object(mesh)

    if DEBUG:
        mock_canvas = {
            'width': 640,
            'height': 480,
        }
        engine3d.perspective(mock_canvas)
    else:
        eel.start('index.html')


if __name__ == '__main__':
    main()
