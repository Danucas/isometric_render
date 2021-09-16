#!/usr/bin/python3
"""
Projection algorithms for isometric perspective
"""
from tkinter import *
from models.vectors import Vector3D
from models.base import BaseModel
import math


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

    def isometric(self, vertex, width, height):
        """
        Projects on vertex depends on the
        defined inclination
        """
        inc = 0.7
        x, y, z = float(vertex.x), float(vertex.y), float(vertex.z)
        Px = (inc * x) - (inc * y) + (width if width else self.region_width / 2)
        Py = ((1 - inc) * x) + ((1 - inc) * y) - z + (height if height else self.region_height / 2)
        return Vector3D(int(Px), int(Py), 1)

    def perspective(self, vertex, width, height):
        if not self.camera.Z0:
            self.camera.Z0 = (width if width else self.region_width / 2.0) / math.tan((self.camera.fov / 2.0) * math.pi / 180.0)
        Px = vertex.x * self.camera.Z0 / (self.camera.Z0 + vertex.z)
        Py = vertex.y * self.camera.Z0 / (self.camera.Z0 + vertex.z)
        return Vector3D(int(Px), int(Py), 1)
            

class Engine3D():
    projection = None
    screen_dimensions = None
    cameras = []
    objects = []
    canvas = None
    motion_id = None
    click_id = None

    def __init__(self, root, projection_type='isometric', mode='Play'):
        self.root = root
        self.projection = Projection(projection_type=projection_type)

    def scroll_zoom(self, canvas):
        """
        zoom event handler
        """
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


    def setup(self, base_object):
        """Define the params for isometric projection"""
        self.screen_dimensions = {
            "width": self.root.winfo_screenwidth(),
            "height": self.root.winfo_screenheight()
        }

        self.projection.viewport = self.screen_dimensions

        if self.projection.projection_type == 'isometric':
            # Calculate the width and height to fit the screen
            scr_reg_w, scr_reg_h = self.calculate_map_width(base_object)
            # Save the parameters to the Projection instance
            self.projection.region_width = scr_reg_w * self.screen_dimensions.get('width')
            self.projection.region_height = scr_reg_h * self.screen_dimensions.get('height')
        elif self.projection.projection_type == 'perspective':
            if len(self.cameras) > 0:
                self.projection.camera = self.cameras[0]
            else:
                print('Creating Camera at setup...')
                self.cameras = [Camera()]
                self.projection.camera = self.cameras[0]
            self.projection.region_width = self.screen_dimensions.get('width')
            self.projection.region_height = self.screen_dimensions.get('height')

        # Define screen dimensions
        self.canvas = Canvas(
            self.root,
            width=self.screen_dimensions["width"],
            height=self.screen_dimensions["height"],
            scrollregion=[
                0, 0,
                self.projection.region_width,
                self.projection.region_height
            ]
        )
        self.canvas.place(x=0, y=0)
        self.canvas.xview_moveto(0.5)
        self.canvas.yview_moveto(0.5)


    def render(self):
        """
        Draw the isometric grid in red
        using the projected vertex
        """
        def getTileSize():
            """
            Get the tile dimensions to calculate the events
            and engine behavior
            """
            try:
                box = self.canvas.bbox(1)
                w = box[2] - box[0]
                h = box[3] - box[1]
                print("Tile size: ", w, h)
                return (w, h)
            except:
                pass

        def color_tile(evn, color):
            """
            Fill a hovered tile with color
            """
            item = self.canvas.find_closest(self.canvas.canvasx(evn.x), self.canvas.canvasy(evn.y), halo=None, start=None)
            if act_tile[0] is not None and item[0] is not None:
                self.canvas.config(cursor="hand2")
                if act_tile[0] != item[0]:
                    self.canvas.config
                    self.canvas.itemconfigure(act_tile[0], fill="red")
                    clicked[0] = False
                else:
                    if clicked[0] is not None and clicked[0] != act_tile[0]:
                        self.canvas.itemconfigure(item[0], fill=color)
            elif item[0] is None:
                self.canvas.config(cursor="")
            act_tile[0] = item[0]

        # Motion Listener
        def tile_mot(evn):
            """
            Fill a selected tile
            """
            color_tile(evn, "blue")

        # Click Listener
        def tile_click(evn):
            """
            Detect click on any tile
            """
            item = self.canvas.find_closest(self.canvas.canvasx(evn.x), self.canvas.canvasy(evn.y), halo=None, start=None)
            bbox = self.canvas.bbox(item[0])
            self.canvas.itemconfigure(item[0], fill="#cffc03")
            clicked[0] = item[0]
            print(item[0], normalized_view[item[0] - 1])
            print("x, y view: ", self.canvas.canvasx(evn.x), self.canvas.canvasy(evn.y))

        self.canvas.delete('all')

        # Draw polygons for each object
        for obj in self.objects:
            print('Rendering: ', obj)
            world_transformation = obj.translate(
                    obj.rotate(obj.vertices)
                )
            camera_transformation = obj.rotate(
                obj.translate(world_transformation, Vector3D(
                    -self.projection.camera.translation.x,
                    -self.projection.camera.translation.y,
                    -self.projection.camera.translation.z
                )), Vector3D(
                        -self.projection.camera.rotation.x,
                        -self.projection.camera.rotation.y,
                        -self.projection.camera.rotation.z
                    )
            )
            projected_view = self.projection.project_all(camera_transformation)
            normalized_view = obj.normalize(
                projected_view, self.projection.viewport
            )
            for face in obj.faces:
                poly = []
                for vertex_index in face:
                    if vertex_index < len(normalized_view) and vertex_index > -1:
                        poly.append(normalized_view[vertex_index].x)
                        poly.append(normalized_view[vertex_index].y)
                    poly.append(poly[0])
                    poly.append(poly[1])
                self.canvas.create_polygon(poly, fill=obj.color, outline="black")

        bbcan = [None]
        act_tile = [None]
        clicked  = [None]

        # # Bind event listeners
        # if self.motion_id:
        #     self.canvas.unbind("<Motion>", self.motion_id)
        #     self.canvas.unbind("<Button-1>", self.click_id)
        # self.motion_id = self.canvas.bind("<Motion>", tile_mot)
        # self.click_id = self.canvas.bind("<Button-1>", tile_click)

        tile_size = getTileSize()
        scroll_view = self.scroll_zoom(self.canvas)
        return tile_size

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


class Camera(BaseModel):
    Z0 = None
    fov = None
    target = None
    upside = None


    def __init__(self, position, fov=45.0, *args, **kwargs):
        super().__init__('Camera', position=position, rotation=Vector3D(3.1416, 0, 0))
        self.fov = fov
        self.upside = Vector3D(
            self.position.x,
            self.position.y + 10,
            self.position.z
        )

    
    def __str__(self):
        return """{}
        Position: {}
        Translation: {}
        Rotation: {}
        """.format(self.id, self.position, self.translation, self.rotation)
