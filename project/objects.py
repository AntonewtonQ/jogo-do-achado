class GameObject:
    def __init__(self, x, y, z, size):
        self.x = x
        self.y = y
        self.z = z
        self.size = size

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glutSolidCube(self.size)
        glPopMatrix()
