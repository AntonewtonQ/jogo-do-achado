class Camera:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def apply(self):
        gluLookAt(self.x, self.y, self.z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
