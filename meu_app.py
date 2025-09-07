import sys
sys.path.append('.')
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple

from screens.setpixel import criar_tela_setpixel
from screens.translacao_2d import criar_tela_translacao
from screens.escala_2d import criar_tela_escala
from services.visualizacao_opengl import OpenGLCanvas
from services.transformacoes import aplicar_translacao, aplicar_escala
from utils.points import parse_points

Point = Tuple[float, float]
PONTOS_PADRAO: List[Point] = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]


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

btn_dda = tk.Button(tela_basicos, text="DDA", width=20, command=lambda: mostrar_mensagem("DDA"))
btn_dda.pack(pady=5)

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
    command=lambda: (janela.geometry("1200x700"), mostrar_frame(tela_transformacoes_2d)),
)
btn_transformacoes.pack(pady=5)

btn_voltar_2d = tk.Button(tela_2d, text="Voltar", width=10, command=lambda: mostrar_frame(tela_inicial))
btn_voltar_2d.pack(pady=20)

tela_transformacoes_2d = tk.Frame(janela)
tela_transformacoes_2d.grid(row=0, column=0, sticky="nsew")

lbl_transformacoes = tk.Label(tela_transformacoes_2d, text="Transformações 2D", font=("Helvetica", 14))
lbl_transformacoes.pack(pady=15)

content_frame = tk.Frame(tela_transformacoes_2d)
content_frame.pack(fill=tk.BOTH, expand=True)

sidebar_frame = tk.Frame(content_frame, width=300)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

options = ["Translação", "Escala", "Rotaçao", "Reflexão", "Cisalhamento"]

combo = ttk.Combobox(sidebar_frame, values=options, state="readonly", font=("Helvetica", 12))
combo.set(options[0])
combo.pack(pady=(0, 10))

inputs_frame = tk.Frame(sidebar_frame)
inputs_frame.pack(fill=tk.BOTH, expand=True)

canvas_frame = tk.Frame(content_frame, width=810, height=610)
canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
canvas = OpenGLCanvas(canvas_frame, width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)


def atualizar_conteudo(event=None):
    selected = combo.get()
    for widget in inputs_frame.winfo_children():
        widget.destroy()

    if selected == "Translação":

        tk.Label(inputs_frame, text="Parâmetros de Translação", font=("Helvetica", 14)).pack(pady=10)
        frame_tx = tk.Frame(inputs_frame)
        frame_tx.pack(pady=5)
        tk.Label(frame_tx, text="Tx:", font=("Helvetica", 12)).grid(row=0, column=0)
        entrada_tx = tk.Entry(frame_tx, width=10, font=("Helvetica", 12))
        entrada_tx.insert(0, "0.2")
        entrada_tx.grid(row=0, column=1, padx=10)

        frame_ty = tk.Frame(inputs_frame)
        frame_ty.pack(pady=5)
        tk.Label(frame_ty, text="Ty:", font=("Helvetica", 12)).grid(row=0, column=0)
        entrada_ty = tk.Entry(frame_ty, width=10, font=("Helvetica", 12))
        entrada_ty.insert(0, "0.1")
        entrada_ty.grid(row=0, column=1, padx=10)

        tk.Label(inputs_frame, text="Pontos (padrão: quadrado)", font=("Helvetica", 12)).pack(pady=10)
        text_pontos = tk.Text(inputs_frame, height=5, width=40, font=("Helvetica", 10))
        pontos_str = "\n".join([f"({x}, {y})" for x, y in PONTOS_PADRAO])
        text_pontos.insert(tk.END, pontos_str)
        text_pontos.pack(pady=5)

        def aplicar_translacao_local():
            try:
                tx = float(entrada_tx.get())
                ty = float(entrada_ty.get())
                try:
                    pontos = parse_points(text_pontos.get("1.0", tk.END))
                except ValueError:
                    pontos = PONTOS_PADRAO
                pontos_transformados = aplicar_translacao(pontos, tx, ty)
                canvas.set_pontos(pontos_transformados)
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos para Tx/Ty.")

        btn_aplicar = tk.Button(inputs_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar_translacao_local)
        btn_aplicar.pack(pady=20)

    elif selected == "Escala":
        tk.Label(inputs_frame, text="Parâmetros de Escala", font=("Helvetica", 14)).pack(pady=10)
        frame_sx = tk.Frame(inputs_frame)
        frame_sx.pack(pady=5)
        tk.Label(frame_sx, text="Sx:", font=("Helvetica", 12)).grid(row=0, column=0)
        entrada_sx = tk.Entry(frame_sx, width=10, font=("Helvetica", 12))
        entrada_sx.insert(0, "1.5")
        entrada_sx.grid(row=0, column=1, padx=10)

        frame_sy = tk.Frame(inputs_frame)
        frame_sy.pack(pady=5)
        tk.Label(frame_sy, text="Sy:", font=("Helvetica", 12)).grid(row=0, column=0)
        entrada_sy = tk.Entry(frame_sy, width=10, font=("Helvetica", 12))
        entrada_sy.insert(0, "0.8")
        entrada_sy.grid(row=0, column=1, padx=10)

        tk.Label(inputs_frame, text="Pontos (padrão: quadrado)", font=("Helvetica", 12)).pack(pady=10)
        text_pontos = tk.Text(inputs_frame, height=5, width=40, font=("Helvetica", 10))
        pontos_str = "\n".join([f"({x}, {y})" for x, y in PONTOS_PADRAO])
        text_pontos.insert(tk.END, pontos_str)
        text_pontos.pack(pady=5)

        def aplicar_escala_local():
            try:
                sx = float(entrada_sx.get())
                sy = float(entrada_sy.get())
                try:
                    pontos = parse_points(text_pontos.get("1.0", tk.END))
                except ValueError:
                    pontos = PONTOS_PADRAO
                pontos_transformados = aplicar_escala(pontos, sx, sy, 0.0, 0.0)
                canvas.set_pontos(pontos_transformados)
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos para Sx/Sy.")

        btn_aplicar = tk.Button(inputs_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar_escala_local)
        btn_aplicar.pack(pady=20)

    else:
        tk.Label(inputs_frame, text=f"{selected} em desenvolvimento", font=("Helvetica", 12)).pack(expand=True)


combo.bind("<<ComboboxSelected>>", atualizar_conteudo)

atualizar_conteudo()

btn_voltar_transformacoes = tk.Button(
    tela_transformacoes_2d,
    text="Voltar",
    width=10,
    command=lambda: (janela.geometry("400x300"), mostrar_frame(tela_2d)),
)
btn_voltar_transformacoes.pack(pady=20)


def mostrar_mensagem(nome):
    popup = tk.Toplevel(janela)
    popup.title(nome)
    popup.geometry("250x100")
    tk.Label(popup, text=f"{nome} em desenvolvimento", font=("Arial", 10)).pack(pady=20)


mostrar_frame(tela_inicial)

janela.mainloop()

