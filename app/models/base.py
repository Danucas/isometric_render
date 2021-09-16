"""
Defines the base's model default attributes
"""

import uuid
from models.vectors import Vector3D
import math


def generate_asset_id(asset_type):
    return '{}_{}'.format(asset_type, uuid.uuid4().hex)

circumference = math.pi * 2


class BaseModel():
    """Base Model"""
    id = None
    position = None
    _rotation = None
    translation = None
    width = None
    height = None

    def __init__(
        self,
        asset_type,
        position=Vector3D(0, 0, 0),
        translation=Vector3D(0, 0, 0),
        rotation=Vector3D(0, 0, 0),
        width=None, height=None):
        """
        Creates a new instance
        """
        self.id = generate_asset_id(asset_type)
        self.position = position
        self.translation = translation
        self.rotation = rotation
        self.width = width
        self.height = height
    
    def __str__(self):
        """String repr"""
        return '{} position: {}'.format(self.id, self.position)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, vector):
        vector = self.validate_rotation_vector(vector)
        self._rotation = vector
    
    def validate_rotation_vector(self, vector):
        if vector.x > circumference:
            vector.x = 0
        elif vector.x < 0:
            vector.x = circumference
        if vector.y > circumference:
            vector.y = 0
        elif vector.y < 0:
            vector.y = circumference
        if vector.z > circumference:
            vector.z = 0
        elif vector.z < 0:
            vector.z = circumference
        return vector
