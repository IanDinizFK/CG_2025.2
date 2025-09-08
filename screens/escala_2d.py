import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple

from services.transformacoes import aplicar_escala
from services.visualizacao_opengl import OpenGLCanvas
from screens.points_editor import PointsEditor
from utils.points import normalize_points

Point = Tuple[float, float]

PONTOS_PADRAO: List[Point] = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]


def criar_tela_escala(root, voltar_callback):
    root.geometry("1200x700")

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Escala 2D", font=("Helvetica", 20)).pack(pady=20)

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(main_frame, width=400)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text="Parâmetros de Escala", font=("Helvetica", 14)).pack(pady=10)

    frame_sx = tk.Frame(left_frame)
    frame_sx.pack(pady=5)
    tk.Label(frame_sx, text="Sx:", font=("Helvetica", 12)).grid(row=0, column=0)
    entrada_sx = tk.Entry(frame_sx, width=10, font=("Helvetica", 12))
    entrada_sx.insert(0, "1.5")
    entrada_sx.grid(row=0, column=1, padx=10)

    frame_sy = tk.Frame(left_frame)
    frame_sy.pack(pady=5)
    tk.Label(frame_sy, text="Sy:", font=("Helvetica", 12)).grid(row=0, column=0)
    entrada_sy = tk.Entry(frame_sy, width=10, font=("Helvetica", 12))
    entrada_sy.insert(0, "0.8")
    entrada_sy.grid(row=0, column=1, padx=10)

    tk.Label(left_frame, text="Centro de Escala", font=("Helvetica", 12)).pack(pady=10)
    frame_centro = tk.Frame(left_frame)
    frame_centro.pack(pady=5)
    tk.Label(frame_centro, text="Cx:", font=("Helvetica", 12)).grid(row=0, column=0)
    entrada_cx = tk.Entry(frame_centro, width=10, font=("Helvetica", 12))
    entrada_cx.insert(0, "0.0")
    entrada_cx.grid(row=0, column=1, padx=10)
    tk.Label(frame_centro, text="Cy:", font=("Helvetica", 12)).grid(row=0, column=2)
    entrada_cy = tk.Entry(frame_centro, width=10, font=("Helvetica", 12))
    entrada_cy.insert(0, "0.0")
    entrada_cy.grid(row=0, column=3, padx=10)

    # Editor de pontos (substitui o campo de texto antigo)
    pontos_editor = PointsEditor(left_frame, initial_points=PONTOS_PADRAO)
    pontos_editor.pack(fill=tk.X, pady=5)

    right_frame = tk.Frame(main_frame, width=800)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas = OpenGLCanvas(right_frame, width=800, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.set_pontos(PONTOS_PADRAO)

    def aplicar():
        try:
            sx = float(entrada_sx.get())
            sy = float(entrada_sy.get())
            cx = float(entrada_cx.get())
            cy = float(entrada_cy.get())
            pontos = pontos_editor.get_points() or PONTOS_PADRAO
            pontos_transformados = aplicar_escala(pontos, sx, sy, cx, cy)
            pontos_transformados = normalize_points(pontos_transformados)
            canvas.set_pontos(pontos_transformados)
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")

    btn_aplicar = tk.Button(left_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar)
    btn_aplicar.pack(pady=20)

    btn_voltar = tk.Button(left_frame, text="Voltar", font=("Helvetica", 12), command=voltar_callback)
    btn_voltar.pack(pady=10)
