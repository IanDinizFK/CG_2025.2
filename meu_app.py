import os
import sys
import platform

sys.path.append('.')
so = platform.system()
if so == "Linux":
    os.environ['PYOPENGL_PLATFORM'] = 'glx'

import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
from screens.transformacoes import criar_tela_transformacoes_2d
from services.visualizacao_opengl import OpenGLCanvas
from screens.points_editor import PointsEditor
from screens.setpixel import criar_tela_setpixel
from screens.circle_midpoint import criar_tela_circulo
from DDA import DDA
from PontoMedio import pmedio

Point = Tuple[float, float]
PONTOS_PADRAO: List[Point] = [(-0.25, -0.25), (0.25, -0.25), (0.25, 0.25), (-0.25, 0.25)]

def mostrar_frame(frame):
    frame.tkraise()


janela = tk.Tk()
janela.title("Projeto de Computação Gráfica")
janela.geometry("400x300")

janela.rowconfigure(0, weight=1)
janela.columnconfigure(0, weight=1)

tela_inicial = tk.Frame(janela)
tela_inicial.grid(row=0, column=0, sticky="nsew")

titulo = tk.Label(tela_inicial, text="Projeto de Computação Gráfica", font=("Helvetica", 16))
titulo.pack(pady=20)

btn_basicos = tk.Button(tela_inicial, text="Básicos", width=20, command=lambda: mostrar_frame(tela_basicos))
btn_basicos.pack(pady=10)

btn_2d = tk.Button(tela_inicial, text="2D", width=20, command=lambda: mostrar_frame(tela_2d))
btn_2d.pack(pady=10)

btn_3d = tk.Button(tela_inicial, text="3D", width=20, command=lambda: mostrar_mensagem("3D"))
btn_3d.pack(pady=10)

tela_basicos = tk.Frame(janela)
tela_basicos.grid(row=0, column=0, sticky="nsew")

lbl_basicos = tk.Label(tela_basicos, text="Operações Básicas", font=("Helvetica", 14))
lbl_basicos.pack(pady=15)

btn_setpixel = tk.Button(
    tela_basicos,
    text="SetPixel",
    width=20,
    command=lambda: criar_tela_setpixel(janela, lambda: mostrar_frame(tela_basicos)),
)
btn_setpixel.pack(pady=5)

btn_dda = tk.Button(tela_basicos, text="DDA", width=20, command=lambda: DDA())
btn_dda.pack(pady=5)

btn_pmedio = tk.Button(tela_basicos, text="Ponto Médio", width=20, command=lambda: pmedio())
btn_pmedio.pack(pady=5)

btn_circulo = tk.Button(tela_basicos, text="Círculo algoritmos", width=20,
                        command=lambda: criar_tela_circulo(janela, lambda: mostrar_frame(tela_basicos)))
btn_circulo.pack(pady=5)

btn_voltar_basicos = tk.Button(tela_basicos, text="Voltar", width=10, command=lambda: mostrar_frame(tela_inicial))
btn_voltar_basicos.pack(pady=20)

tela_2d = tk.Frame(janela)
tela_2d.grid(row=0, column=0, sticky="nsew")

lbl_2d = tk.Label(tela_2d, text="2D", font=("Helvetica", 14))
lbl_2d.pack(pady=15)

btn_transformacoes = tk.Button(
    tela_2d,
    text="Transformações",
    width=20,
    command=lambda: (janela.geometry("1200x700"), mostrar_frame(criar_tela_transformacoes_2d(janela, lambda: (janela.geometry("400x300"), mostrar_frame(tela_2d))))),
)
btn_transformacoes.pack(pady=5)

btn_voltar_2d = tk.Button(tela_2d, text="Voltar", width=10, command=lambda: mostrar_frame(tela_inicial))
btn_voltar_2d.pack(pady=20)


def mostrar_mensagem(nome):
    popup = tk.Toplevel(janela)
    popup.title(nome)
    popup.geometry("250x100")
    tk.Label(popup, text=f"{nome} em desenvolvimento", font=("Arial", 10)).pack(pady=20)

mostrar_frame(tela_inicial)

janela.mainloop()
