from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from typing import List, Tuple

Point = Tuple[float, float]

class OpenGLCanvas(OpenGLFrame):
    def __init__(self, *args, width=800, height=600, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.bind("<Configure>", self._on_configure)
        self.pontos: List[Point] = []

    def _on_configure(self, evt):
        self.width, self.height = evt.width, evt.height
        try:
            glViewport(0, 0, self.width, self.height)
            self.after(0, self._display)
        except Exception:
            pass

    def initgl(self):
        print("[OpenGLCanvas] initgl: size=", self.width, self.height)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1, 1, -1, 1, -1, 1)
        glMatrixMode(GL_MODELVIEW)

        self.pontos = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
        try:
            self.after(0, self._display)
        except Exception:
            pass

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        glLineWidth(1.0)
        glPointSize(1.0)

        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex2f(-1.0, 0.0)
        glVertex2f(1.0, 0.0)
        glVertex2f(0.0, -1.0)
        glVertex2f(0.0, 1.0)
        glEnd()

        glColor3f(0.0, 0.0, 0.0)
        if self.pontos:
            glBegin(GL_LINE_LOOP if len(self.pontos) > 2 else GL_LINE_STRIP)
            for x, y in self.pontos:
                glVertex2f(x, y)
            glEnd()

    def set_pontos(self, pontos: List[Point]):
        self.pontos = pontos
        try:
            self._display()
        except Exception:
            self.after(0, self._display)

    def get_pontos(self) -> List[Point]:
        return list(self.pontos)
