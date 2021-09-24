#!/usr/bin/python3
"""
Projection algorithms for isometric perspective
"""
from models.base import BaseModel
import math
import numpy as np


class Projection():
    projection_type = None
    region_width = None
    region_height = None
    viewport = None
    camera = None

    def __init__(self, projection_type='isometric'):
        self.projection_type = projection_type

    def project_all(self, vertices):
        """
        Project all vertex from object
        """
        projected = []
        for vertex in vertices:
            projected.append(self.project(vertex))
        return projected


    def project(self, vertex, width=None, height=None):
        if self.projection_type == 'isometric':
            return self.isometric(vertex, width, height)
        elif self.projection_type == 'perspective':
            return self.perspective(vertex, width, height)
        elif self.projection_type == 'ortho':
            return self.ortho(vertex, width, height)


    def isometric(self, vertex, width, height):
        """
        Projects on vertex depends on the
        defined inclination
        """
        inc = 0.7
        x, y, z = float(vertex[0]), float(vertex[1]), float(vertex[2])
        Px = (inc * x) - (inc * y) + (width if width else self.region_width / 2)
        Py = ((1 - inc) * x) + ((1 - inc) * y) - z + (height if height else self.region_height / 2)
        return np.array([int(Px), int(Py), 1])


    def perspective(self, vertex, width, height):
        if not self.camera.Z0:
            self.camera.Z0 = (width if width else self.region_width / 2.0) / math.tan((self.camera.fov / 2.0) * math.pi / 180.0)
        Px = vertex[0] * self.camera.Z0 / (self.camera.Z0 + vertex[2])
        Py = vertex[1] * self.camera.Z0 / (self.camera.Z0 + vertex[2])
        
        return np.array([int(Px), int(Py), vertex[2]])

    def ortho(self, vertex, width, height):
        pass


class Engine3D():
    projection = None
    screen_dimensions = None
    cameras = []
    objects = []
    canvas = None
    motion_id = None
    click_id = None

    def __init__(self, projection_type='isometric', mode='Play'):
        self.projection = Projection(projection_type=projection_type)


    def calculate_map_width(self, terrain):
        """
        Get the width for the entire isometric map to fit the screen
        """
        fs = terrain.faces
        vr = terrain.vertices
        pos = fs[0][3] - 1
        w1 = self.screen_dimensions["width"]
        h1 = self.screen_dimensions["height"]
        x1 = self.projection.project(vr[len(vr) - 1 - pos], width=w1, height=h1).x
        x2 = self.projection.project(vr[pos], width=w1, height=h1).x
        y1 = self.projection.project(vr[0], width=w1, height=h1).y
        y2 = self.projection.project(vr[len(vr) - 1], width=w1, height=h1).y
        w = x1 - x2
        h = y1 - y2
        return int((w / self.screen_dimensions["width"])) + 2, int((h / self.screen_dimensions["height"])) + 2


    def raytrace(self, canvas_dimensions):
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


    def wireframe(self, projection_type, canvas_dimensions):
        """
        Draw the isometric grid in red
        using the projected vertex
        """
        # Configure viewportself.screen_dimensions = {
        self.screen_dimensions = {
            "width": canvas_dimensions['width'],
            "height": canvas_dimensions['height']
        }

        self.projection.viewport = self.screen_dimensions
        self.projection.projection_type = projection_type
        self.projection.camera = self.cameras[0]
        self.projection.region_width = self.screen_dimensions.get('width')
        self.projection.region_height = self.screen_dimensions.get('height')

        # Draw polygons for each object
        projected_objects = []
        for obj in self.objects:
            print('Rendering: ', obj)

            world_transformation = obj.translate(
                    obj.rotate(obj.scale(obj.vertices))
                )
            camera_transformation = obj.rotate(
                obj.translate(world_transformation, np.array(
                    [
                        -self.projection.camera.translation[0],
                        -self.projection.camera.translation[1],
                        -self.projection.camera.translation[2]
                    ]
                )), np.array(
                        [
                            -self.projection.camera.rotation[0],
                            -self.projection.camera.rotation[1],
                            -self.projection.camera.rotation[2]
                        ]
                        
                    )
            )
            projected_view = self.projection.project_all(camera_transformation)
            normalized_view = obj.normalize(
                projected_view, self.projection.viewport
            )
            projected_faces = []
            for face in obj.faces:
                poly = []
                for vertex_index in face:
                    poly.append(
                        [
                            int(normalized_view[vertex_index][0]),
                            int(normalized_view[vertex_index][1]),
                            int(camera_transformation[vertex_index][2])
                        ]
                    )
                projected_faces.append(poly)
            center = list(obj.calculate_center(normalized_view))
            vertices = [ [int(p[0]), int(p[1]), int(p[2])] for p in normalized_view]
            # print('calculated_center: ', center)
            # print(''vertices)
            projected_objects.append({
                'vertices': vertices,
                'faces': obj.clip(self.projection.camera.translation, projected_faces),
                'center': [ int(coord) for coord in obj.calculate_center(normalized_view) ],
            })
        print(projected_objects[0]['faces'][:20])
        return projected_objects

    def add_camera(self, camera):
        self.cameras.append(camera)

    def add_object(self, obj):
        self.objects.append(obj)

    def __str__(self):
        return """
        Engine 3D
        v 0.0.1
        viewport: {} x {}
        Cameras:
        {}
        Objects:
        {}
        """.format(
            self.screen_dimensions.get('width'),
            self.screen_dimensions.get('heiht'),
            [str(cam) for cam in self.cameras],
            [str(obj) for obj in self.objects]
        )
