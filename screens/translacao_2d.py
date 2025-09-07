import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple

from services.transformacoes import aplicar_translacao
from services.visualizacao_opengl import OpenGLCanvas
from utils.points import parse_points

Point = Tuple[float, float]

PONTOS_PADRAO: List[Point] = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]


def criar_tela_translacao(root, voltar_callback):
    root.geometry("1200x700") 

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Translação 2D", font=("Helvetica", 20)).pack(pady=20)

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(main_frame, width=400)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text="Parâmetros de Translação", font=("Helvetica", 14)).pack(pady=10)

    frame_tx = tk.Frame(left_frame)
    frame_tx.pack(pady=5)
    tk.Label(frame_tx, text="Tx:", font=("Helvetica", 12)).grid(row=0, column=0)
    entrada_tx = tk.Entry(frame_tx, width=10, font=("Helvetica", 12))
    entrada_tx.insert(0, "0.2")
    entrada_tx.grid(row=0, column=1, padx=10)

    frame_ty = tk.Frame(left_frame)
    frame_ty.pack(pady=5)
    tk.Label(frame_ty, text="Ty:", font=("Helvetica", 12)).grid(row=0, column=0)
    entrada_ty = tk.Entry(frame_ty, width=10, font=("Helvetica", 12))
    entrada_ty.insert(0, "0.1")
    entrada_ty.grid(row=0, column=1, padx=10)

    tk.Label(left_frame, text="Pontos (padrão: quadrado)", font=("Helvetica", 12)).pack(pady=10)
    text_pontos = tk.Text(left_frame, height=5, width=40, font=("Helvetica", 10))
    pontos_str = "\n".join([f"({x}, {y})" for x, y in PONTOS_PADRAO])
    text_pontos.insert(tk.END, pontos_str)
    text_pontos.pack(pady=5)

    right_frame = tk.Frame(main_frame, width=800)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas = OpenGLCanvas(right_frame, width=800, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.set_pontos(PONTOS_PADRAO) 

    def aplicar():
        try:
            tx = float(entrada_tx.get())
            ty = float(entrada_ty.get())
            pontos_txt = text_pontos.get("1.0", tk.END)
            try:
                pontos = parse_points(pontos_txt)
            except ValueError:
                pontos = PONTOS_PADRAO
            pontos_transformados = aplicar_translacao(pontos, tx, ty)
            canvas.set_pontos(pontos_transformados)
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos para Tx ou Ty.")

    btn_aplicar = tk.Button(left_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar)
    btn_aplicar.pack(pady=20)

    btn_voltar = tk.Button(left_frame, text="Voltar", font=("Helvetica", 12), command=voltar_callback)
    btn_voltar.pack(pady=10)

