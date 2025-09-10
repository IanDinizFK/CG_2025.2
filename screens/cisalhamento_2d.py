import tkinter as tk
from tkinter import messagebox
from typing import List, Tuple

from services.transformacoes import aplicar_cisalhamento
from services.visualizacao_opengl import OpenGLCanvas
from screens.points_editor import PointsEditor
from utils.points import normalize_points

Point = Tuple[float, float]

# Pontos padrão de um quadrado
PONTOS_PADRAO: List[Point] = [(-0.25, -0.25), (0.25, -0.25), (0.25, 0.25), (-0.25, 0.25)]


def criar_tela_cisalhamento(root, voltar_callback):
    root.geometry("1200x700")

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Cisalhamento 2D", font=("Helvetica", 20)).pack(pady=20)

    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    left_frame = tk.Frame(main_frame, width=400)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(left_frame, text="Parâmetros de Cisalhamento", font=("Helvetica", 14)).pack(pady=10)

    # ShX
    frame_shx = tk.Frame(left_frame)
    frame_shx.pack(pady=5)
    tk.Label(frame_shx, text="ShX:", font=("Helvetica", 12)).grid(row=0, column=0)
    entrada_shx = tk.Entry(frame_shx, width=10, font=("Helvetica", 12))
    entrada_shx.insert(0, "0.0")
    entrada_shx.grid(row=0, column=1, padx=10)

    # ShY
    frame_shy = tk.Frame(left_frame)
    frame_shy.pack(pady=5)
    tk.Label(frame_shy, text="ShY:", font=("Helvetica", 12)).grid(row=0, column=0)
    entrada_shy = tk.Entry(frame_shy, width=10, font=("Helvetica", 12))
    entrada_shy.insert(0, "0.0")
    entrada_shy.grid(row=0, column=1, padx=10)

    # --- Centro de Cisalhamento ---
    tk.Label(left_frame, text="Centro de Cisalhamento", font=("Helvetica", 12)).pack(pady=10)
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


    def aplicar():
        try:
            shx = float(entrada_shx.get()) / 10.0
            shy = float(entrada_shy.get()) / 10.0
            cx = float(entrada_cx.get())
            cy = float(entrada_cy.get())
            pontos = pontos_editor.get_points() or PONTOS_PADRAO
            pontos_transformados = aplicar_cisalhamento(pontos, shx, shy, cx, cy)
            pontos_transformados = normalize_points(pontos_transformados)
            canvas.set_pontos(pontos_transformados)
        except ValueError:
            messagebox.showerror("Erro", "Valores inválidos.")


    btn_aplicar = tk.Button(left_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar)
    btn_aplicar.pack(pady=5)

    pontos_editor = PointsEditor(left_frame, initial_points=PONTOS_PADRAO)
    pontos_editor.pack(fill=tk.X, pady=5)

    def atualizar_pontos():
        try:
            pontos = pontos_editor.get_points()
            if not pontos:
                pontos = PONTOS_PADRAO
            pontos = normalize_points(pontos)
            canvas.set_pontos(pontos)
        except ValueError:
            messagebox.showerror("Erro", "Pontos inválidos no editor.")

    btn_atualizar = tk.Button(left_frame, text="Atualizar Pontos", font=("Helvetica", 12), command=atualizar_pontos)
    btn_atualizar.pack(pady=5)

    right_frame = tk.Frame(main_frame, width=800)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas = OpenGLCanvas(right_frame, width=800, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.set_pontos(PONTOS_PADRAO)

    btn_voltar = tk.Button(left_frame, text="Voltar", font=("Helvetica", 12), command=voltar_callback)
    btn_voltar.pack(pady=10)
