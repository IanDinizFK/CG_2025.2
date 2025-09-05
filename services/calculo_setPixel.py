import pyglet
from OpenGL.GL import *
from OpenGL.GLU import *

def desenhar_com_opengl(largura_tela, altura_tela, x_pixel, y_pixel):
    janela = pyglet.window.Window(largura_tela, altura_tela, "Visualização OpenGL do Pixel")

    @janela.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        gl_x = (x_pixel / largura_tela) * 2.0 - 1.0
        gl_y = 1.0 - (y_pixel / altura_tela) * 2.0

        glPointSize(1.0)

        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_POINTS)
        glVertex2f(gl_x, gl_y)
        glEnd()

    pyglet.app.run()

def setPixel(xmin, ymin, xmax, ymax, x, y, ndh, ndv, opcao):
    ndc = inp_to_ndc(x, y, xmin, xmax, ymin, ymax, opcao)
    dc = ndc_to_dc(ndh, ndv, ndc[0], ndc[1], opcao)
    string =  "Função SetPixel\n\n"
    if(opcao == 0):
        string += "1. Transformação User -> NDC (para cenário [0,1])\n"
        string += "   Fórmula X_ndc = (x - xmin)/(xmax - xmin) \n"
        string += "   Fórmula Y_ndc = (y - ymin)/(ymax - ymin) \n"
        string += f"   X_ndc = ({x} - {xmin})/({xmax} - {xmin}) = {round(ndc[0],2)}\n"
        string += f"   Y_ndc = ({y} - {ymin})/({ymax} - {ymin}) = {round(ndc[1],2)}\n\n"
    else:
        string += "1. Transformação User -> NDC (para cenário [-1,1])\n"
        string += "   Fórmula X_ndc = (2*(x - xmin))/((xmax - xmin))- 1  \n"
        string += "   Fórmula Y_ndc = (2*(y - ymin))/((ymax - ymin))- 1 \n"
        string += f"   X_ndc = (2*({x} - {xmin}))/(({xmax} - {xmin}))- 1 = {round(ndc[0],2)}\n"
        string += f"   Y_ndc = (2*({y} - {ymin}))/(({ymax} - {ymin}))- 1 = {round(ndc[1],2)}\n\n"

    
    if(opcao == 0):
        string += "2. Transformação NDC -> DC [0, 1]\n"
        string += "   Fórmula X_pixel = ndc_x * (ndh - 1) \n"
        string += "   Fórmula Y_pixel = ndc_y * (ndv - 1) \n"
        string += f"   X_pixel = {ndc[0]} * ({ndh} - 1) = {round(dc[0],2)}\n"
        string += f"   Y_pixel = {ndc[1]} * ({ndv} - 1) = {round(dc[1],2)}\n"
    else:
        string += "2. Transformação NDC -> DC [-1, 1]\n"
        string += "   Fórmula X_pixel = ((ndx + 1)/2) * (ndh - 1)\n"
        string += "   Fórmula Y_pixel = ((ndy + 1)/2) * (ndv - 1)\n"
        string += f"   X_pixel = (({ndc[0]} + 1)/2) * ({ndh} - 1) = {round(dc[0],2)}\n"
        string += f"   Y_pixel = (({ndc[1]} + 1)/2) * ({ndv} - 1) = {round(dc[1],2)}\n"
    desenhar_com_opengl(ndh, ndv, dc[0], dc[1])
    return string

def inp_to_ndc(x,y, xmin,xmax, ymin,ymax, opcao):
    if(opcao == 0):
        ndcx = (x - xmin)/(xmax - xmin)
        ndcy = (y - ymin)/(ymax - ymin)
    else:
        ndcx = (2*(x - xmin))/((xmax - xmin))- 1
        ndcy = (2*(y - ymin))/((ymax - ymin))- 1
    return ndcx, ndcy

def ndc_to_dc(ndh, ndv, ndcx, ndcy, opcao):
    if(opcao == 0):
        dcx = round(ndcx * (ndh - 1))
        dcy = round(ndcy * (ndv - 1))
    else:
        dcx = round(((ndcx + 1)/2) * (ndh - 1))
        dcy = round(((ndcy + 1)/2) * (ndv - 1))
    return dcx, dcy