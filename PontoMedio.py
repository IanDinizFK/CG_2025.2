import os

from tkinter import * 
from OpenGL.GL import *
from OpenGL.GLU import *

from utils.point import Point
from utils.windowtk import WindowTk
from tk_widgets.scrollabe_show_result import scrolable_show_result
from algorithms.PontoMedio import drowLine


WIDTH = 800
HEIGHT = 600

def render_config_func():
    glClearColor(1, 1, 1, 1)
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPointSize(1) 

def pmedio():
    global vertices
    vertices = []

    def render_func():
        glClear(GL_COLOR_BUFFER_BIT)

        glColor3f(1, 0, 0)
        glBegin(GL_POINTS)
        for v in vertices:
            glVertex2i(v[0]+1, v[1]+1)
        glEnd()

    root = Tk()
    root.title("Ponto Médio")

    window = WindowTk(root, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
    window.pack(side=RIGHT, expand=True, fill=BOTH, padx=0, pady=0)

    side_frame = Frame(root)
    side_frame.pack(side=LEFT, fill=Y, padx=0, pady=0)  

    Label(side_frame, text="X1").grid(row=0, column=0, padx=5, pady=5)
    x1_entry = Entry(side_frame, width=20)
    x1_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(side_frame, text="Y1").grid(row=1, column=0, padx=5, pady=5)
    y1_entry = Entry(side_frame, width=20)
    y1_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(side_frame, text="X2").grid(row=2, column=0, padx=5, pady=5)
    x2_entry = Entry(side_frame, width=20)
    x2_entry.grid(row=2, column=1, padx=5, pady=5)

    Label(side_frame, text="Y2").grid(row=3, column=0, padx=5, pady=5)
    y2_entry = Entry(side_frame, width=20)
    y2_entry.grid(row=3, column=1, padx=5, pady=5)


    def drow():
        x1 = int(x1_entry.get())
        y1 = int(y1_entry.get())
        x2 = int(x2_entry.get())
        y2 = int(y2_entry.get())

        start = Point(x1, y1)
        end = Point(x2, y2)
        
        globals()["vertices"] = drowLine(start, end)

        scrolable_show_result(side_frame, list=vertices)

    btn_aplicar = Button(side_frame, text="Aplicar", command=drow)
    btn_aplicar.grid(row=5, column=0, columnspan=2, pady=10)


    window.set_init_config(render_config_func)
    window.set_render_config(render_func)
    window.animate = 1
    window.mainloop()
