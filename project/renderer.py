from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw_scene():
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    
    glColor3f(1.0, 0.0, 0.0)  # Vermelho
    glutSolidCube(1)  # Cubo sólido no centro

