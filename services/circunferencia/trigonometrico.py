import pyglet
import math
from OpenGL.GL import *
from OpenGL.GLU import *

def trigonometric_algorithm(radius):
    """
    Executa o algoritmo Trigonométrico com passo fixo de 1 grau.
    Esta versão é a tradução mais direta do conceito matemático e
    gera buracos visíveis em círculos de raio grande.

    Retorna:
        - Uma lista de tuplos (x, y) com os pontos da circunferência.
        - Uma string formatada com alguns passos do cálculo.
    """
    passos_calculo = []
    pontos = []
    
    passos_calculo.append(f"--- Algoritmo Trigonométrico Literal (Passo Fixo de 1 Grau) ---")
    passos_calculo.append(f"Raio={radius}\n")
    passos_calculo.append("Loop de 0 a 359 graus:\n")

    for grau in range(360):
        radiano = math.radians(grau)
        
        x_float = radius * math.cos(radiano)
        y_float = radius * math.sin(radiano)
        
        ponto_atual = (round(x_float), round(y_float))
        
        if not pontos or ponto_atual != pontos[-1]:
            pontos.append(ponto_atual)
        
        if grau < 4 or grau > 355: 
            passos_calculo.append(f"  --- Passo {grau} (Ângulo = {grau}°) ---")
            
            passos_calculo.append(
                f"     x = {radius} * cos({radiano:.4f}) = {x_float:.2f}"
            )
            passos_calculo.append(
                f"     y = {radius} * sin({radiano:.4f}) = {y_float:.2f}"
            )
            passos_calculo.append(f"     Ponto arredondado: {ponto_atual}\n")

        elif grau == 4: 
            passos_calculo.append("  ...\n  (Muitos passos intermédios omitidos para clareza)\n  ...\n")

    string_final = "\n".join(passos_calculo)
    return pontos, string_final

def desenhar_circulo_opengl(largura_tela, altura_tela, xc, yc, pontos_circulo):
    """
    Cria uma janela OpenGL e desenha um círculo usando a lista de pontos pré-calculada.
    """
    janela = pyglet.window.Window(largura_tela, altura_tela, "Círculo - Trigonométrico LITERAL (com falhas)")

    @janela.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        gluOrtho2D(0, largura_tela, 0, altura_tela)
        
        glColor3f(1.0, 0.0, 0.0) 
        glPointSize(2.0)

        glBegin(GL_POINTS)
        for x, y in pontos_circulo:
            glVertex2f(xc + x, yc + y)
        glEnd()

    pyglet.app.run()