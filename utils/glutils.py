from OpenGL.GL import *
from OpenGL.GLU import *

def drowCartesianPlane():
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex2fv([1, 0])
        glVertex2fv([-1, 0])
        glVertex2fv([0, 1])
        glVertex2fv([0, -1])
        glEnd()