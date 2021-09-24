from models.base import BaseModel
import math
import numpy as np

class Camera(BaseModel):
    Z0 = None
    fov = None
    target = None
    upside = None


    def __init__(self, position, fov=45.0, *args, **kwargs):
        super().__init__('Camera', position=position, rotation=np.array([0, 0, 0]))
        self.fov = fov
        self.position = position if position is not None else np.array([0, 0, 0])
        self.upside = np.array(
            [
                self.position[0],
                self.position[1] + 10,
                self.position[2]
            ]
        )
        self.target = np.array(
            [
                self.position[0],
                self.position[1],
                self.position[2] + 10
            ]
        )

    
    def __str__(self):
        return """{}
        Position: {}
        Translation: {}
        Rotation: {}
        """.format(self.id, self.position, self.translation, self.rotation)