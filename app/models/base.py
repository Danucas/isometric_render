"""
Defines the base's model default attributes
"""

import uuid
from models.vectors import Vector3D
import math
import numpy as np


def generate_asset_id(asset_type):
    return '{}_{}'.format(asset_type, uuid.uuid4().hex)

circumference = math.pi * 2


class BaseModel():
    """Base Model"""
    id = None
    position = None
    _rotation = None
    _translation = None
    scalar = None
    width = None
    height = None

    def __init__(
        self,
        asset_type,
        position=np.array([0, 0, 0]),
        translation=np.array([0, 0, 0]),
        scalar=1,
        rotation=np.array([0, 0, 0]),
        width=None, height=None):
        """
        Creates a new instance
        """
        self.id = generate_asset_id(asset_type)
        self.position = position
        self.translation = translation
        self.rotation = rotation
        self.scalar = scalar
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

    @property
    def translation(self):
        return self._translation

    @translation.setter
    def translation(self, vector):
        self._translation = vector
    
    def validate_rotation_vector(self, vector):
        if vector[0] > circumference:
            vector[0] = 0
        elif vector[0] < 0:
            vector[0] = circumference
        if vector[1] > circumference:
            vector[1] = 0
        elif vector[1] < 0:
            vector[1] = circumference
        if vector[2] > circumference:
            vector[2] = 0
        elif vector[2] < 0:
            vector[2] = circumference
        return vector
