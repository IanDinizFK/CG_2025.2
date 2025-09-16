import pyglet
import math
from OpenGL.GL import *
from OpenGL.GLU import *

def polynomial_algorithm(radius):
    """
    Executa o algoritmo Polinomial da forma mais direta (ingénua), sem otimizações.
    Calcula os pontos para toda a extensão de x, de -R a +R.

    Retorna:
        - Uma lista com TODOS os pontos (x, y) da circunferência.
        - Uma string formatada com os passos do cálculo.
    """
    passos_calculo = []
    pontos = []

    passos_calculo.append(f"--- Algoritmo Polinomial Original (sem otimização) ---")
    passos_calculo.append(f"Raio={radius}\n")
    passos_calculo.append(f"Loop de x de {-radius} a {radius}:\n")
    passos_calculo.append("Fórmula: y = +/- sqrt(R² - x²)\n")

    for x in range(-radius, radius + 1):

        valor_dentro_da_raiz = radius**2 - x**2
        if valor_dentro_da_raiz >= 0:
            y_float = math.sqrt(valor_dentro_da_raiz)

            ponto_superior = (x, round(y_float))
            ponto_inferior = (x, -round(y_float))
            
            pontos.append(ponto_superior)
            if y_float != 0:
                pontos.append(ponto_inferior)

            if abs(x) < 4 or abs(x) > radius - 4:
                passos_calculo.append(f"  --- Passo (x = {x}) ---")
                passos_calculo.append(
                    f"     y = +/-sqrt({radius}^2 - {x}^2) = +/-sqrt({valor_dentro_da_raiz}) = +/-{y_float:.2f}"
                )
                passos_calculo.append(f"     Pontos arredondados: {ponto_superior} e {ponto_inferior}\n")
            elif x == 4:
                passos_calculo.append("  ...\n  (Muitos passos intermédios omitidos)\n  ...\n")

    string_final = "\n".join(passos_calculo)
    return pontos, string_final

def desenhar_circulo_opengl(largura_tela, altura_tela, xc, yc, pontos_circulo_completo):
    """
    Cria uma janela OpenGL e desenha um círculo usando a lista completa de pontos.
    """
    janela = pyglet.window.Window(largura_tela, altura_tela, "Círculo - Polinomial ORIGINAL (com falhas)")

    @janela.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        gluOrtho2D(0, largura_tela, 0, altura_tela)

        glColor3f(1.0, 1.0, 0.0) 
        glPointSize(2.0)

        glBegin(GL_POINTS)

        for x, y in pontos_circulo_completo:
            glVertex2f(xc + x, yc + y)
        glEnd()

    pyglet.app.run()


if __name__ == "__main__":
    RAIO = 250
    LARGURA_TELA = 800
    ALTURA_TELA = 600
    CENTRO_X = LARGURA_TELA // 2
    CENTRO_Y = ALTURA_TELA // 2

    pontos_calculados, relatorio_calculo = polynomial_algorithm_original(RAIO)

    print(relatorio_calculo)

    print("\n\nA abrir a janela OpenGL para desenhar...")
    desenhar_circulo_opengl(LARGURA_TELA, ALTURA_TELA, CENTRO_X, CENTRO_Y, pontos_calculados)