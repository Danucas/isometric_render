# Define vector objects


class Vector3D():
    x = None
    y = None
    z = None

    def __init__(self, x, y, z):
        """Vector 3D"""
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        """Vector representation"""
        return 'x: {}, y: {}, z: {}'.format(
            self.x, self.y, self.z
        )

class Triangle(Vector3D):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, context):
        pass
