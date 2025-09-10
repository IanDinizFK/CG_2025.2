import pyglet
import math
from OpenGL.GL import *
from OpenGL.GLU import *

def polynomial_algorithm(radius):
    """
    Executa o algoritmo Polinomial, calculando os pontos para o primeiro octante.

    Retorna:
        - Uma lista de tuplos (x, y) com os pontos do primeiro octante.
        - Uma string formatada com os passos detalhados do cálculo.
    """
    passos_calculo = []
    pontos_octante1 = []

    passos_calculo.append(f"--- Algoritmo Polinomial ---")
    passos_calculo.append(f"Raio={radius}\n")
    passos_calculo.append("Loop de x de 0 até y (cálculo do 1º octante):\n")

    x = 0
    y = float(radius)

    k = 0
    while x <= y:
        ponto_atual = (x, round(y))
        pontos_octante1.append(ponto_atual)
        if k < 4 or abs(x - y) < 2:
            passos_calculo.append(f"  --- Passo {k} (x = {x}) ---")

            passos_calculo.append(
                f"     y = sqrt({radius}^2 - {x}^2) = sqrt({radius**2} - {x**2}) = {y:.2f}"
            )
            passos_calculo.append(f"     Ponto arredondado: {ponto_atual}\n")

        elif k == 4:
            passos_calculo.append("  ...\n  (Muitos passos intermédios omitidos)\n  ...\n")

        x += 1
        if radius**2 - x**2 >= 0:
            y = math.sqrt(radius**2 - x**2)
        else:
            break
        k += 1

    string_final = "\n".join(passos_calculo)
    return pontos_octante1, string_final

def desenhar_circulo_opengl(largura_tela, altura_tela, xc, yc, pontos_octante1):
    """
    Cria uma janela OpenGL e desenha um círculo usando os pontos pré-calculados
    do primeiro octante, espelhando-os para formar o círculo completo.
    """
    janela = pyglet.window.Window(largura_tela, altura_tela, "Círculo - Algoritmo Polinomial")

    @janela.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        gluOrtho2D(0, largura_tela, 0, altura_tela)
        
        glColor3f(1.0, 0.0, 1.0) 
        glPointSize(2.0)

        glBegin(GL_POINTS)
        for x, y in pontos_octante1:
            glVertex2f(xc + x, yc + y)
            glVertex2f(xc - x, yc + y)
            glVertex2f(xc + x, yc - y)
            glVertex2f(xc - x, yc - y)
            glVertex2f(xc + y, yc + x)
            glVertex2f(xc - y, yc + x)
            glVertex2f(xc + y, yc - x)
            glVertex2f(xc - y, yc - x)
        glEnd()

    pyglet.app.run()