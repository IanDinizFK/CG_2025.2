import os

from tkinter import *
from pyopengltk import OpenGLFrame
from OpenGL.GL import *   

class WindowTk(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._render = lambda: None
        self._init_config = lambda: None

    def initgl(self):
        self._init_config()

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self._render()
        glFlush()
    
    def set_render_config(self, func):
        self._render = func

    def set_init_config(self, func):
        self._init_config = func
