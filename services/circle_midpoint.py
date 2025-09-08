import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(x, y)
    glEnd()

def draw_circle_symmetry(x, y):
    draw_pixel(x, y)
    draw_pixel(y, x)
    draw_pixel(y, -x)
    draw_pixel(x, -y)
    draw_pixel(-x, -y)
    draw_pixel(-y, -x)
    draw_pixel(-y, x)
    draw_pixel(-x, y)

def circle_midpoint(radius):
    points = []
    x = 0
    y = radius
    d = 5/4 - radius

    points.append((x, y))
    draw_circle_symmetry(x, y)

    while y > x:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        points.append((x, y))
        draw_circle_symmetry(x, y)
    return points

def desenhar_circulo_opengl(largura_tela, altura_tela, raio):
    janela = pyglet.window.Window(largura_tela, altura_tela, "Círculo Ponto Médio")

    @janela.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        # Configura coordenadas centradas
        gluOrtho2D(-largura_tela//2, largura_tela//2, -altura_tela//2, altura_tela//2)

        glPointSize(2.0)
        circle_midpoint(raio)

    pyglet.app.run()
