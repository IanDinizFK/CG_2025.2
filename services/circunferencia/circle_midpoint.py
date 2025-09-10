import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *

def _draw_pixel(x, y):
    """Função interna para desenhar um ponto em coordenadas já transladadas."""
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def midpoint_algorithm(radius):
    """
    Executa o Algoritmo do Ponto Médio.

    Retorna:
        - Uma lista de tuplos (x, y) com os pontos do primeiro octante.
        - Uma string formatada com todos os passos do cálculo.
    """
    passos_calculo = []
    pontos_octante1 = []
    
    x = 0
    y = radius
    d = 1 - radius

    passos_calculo.append(f"Início: x={x}, y={y}, Raio={radius}")
    passos_calculo.append(f"   d inicial = 1 - R = 1 - {radius} = {d}\n")

    pontos_octante1.append((x, y))

    while y > x:
        passos_calculo.append(f"Loop: x={x}, y={y}, d={d}")
        
        if d < 0:
            d_antigo = d
            d += 2 * x + 3
            passos_calculo.append(f"   d < 0, escolhe E.")
            passos_calculo.append(f"   d_novo = d + 2*x + 3 = {d_antigo} + 2*{x} + 3 = {d}")
        else:
            d_antigo = d
            d += 2 * (x - y) + 5
            y -= 1
            passos_calculo.append(f"   d >= 0, escolhe SE.")
            passos_calculo.append(f"   d_novo = d + 2*(x - y) + 5 = {d_antigo} + 2*({x} - {y+1}) + 5 = {d}")
            passos_calculo.append(f"   y_novo = y - 1 = {y}")

        x += 1
        passos_calculo.append(f"   x_novo = x + 1 = {x}\n")
        pontos_octante1.append((x, y))
    
    string_final = "\n".join(passos_calculo)
    return pontos_octante1, string_final


def desenhar_circulo_opengl(largura_tela, altura_tela, xc, yc, pontos_octante1):
    """
    Cria uma janela OpenGL e desenha um círculo usando os pontos pré-calculados.
    """
    janela = pyglet.window.Window(largura_tela, altura_tela, "Círculo - Ponto Médio (OpenGL)")

    @janela.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        gluOrtho2D(0, largura_tela, 0, altura_tela)

        glColor3f(0.0, 1.0, 0.0)
        glPointSize(2.0)

        for x, y in pontos_octante1:
            _draw_pixel(xc + x, yc + y)
            _draw_pixel(xc - x, yc + y)
            _draw_pixel(xc + x, yc - y)
            _draw_pixel(xc - x, yc - y)
            _draw_pixel(xc + y, yc + x)
            _draw_pixel(xc - y, yc + x)
            _draw_pixel(xc + y, yc - x)
            _draw_pixel(xc - y, yc - x)

    pyglet.app.run()