import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Tuple

from services.transformacoes import aplicar_translacao, aplicar_escala, aplicar_cisalhamento
from services.visualizacao_opengl import OpenGLCanvas
from screens.points_editor import PointsEditor

from utils.CGmatriz import CGMatriz
from utils.points import normalize_points
from utils.matrix import translation_matrix, scale_matrix, apply_matrix_point, multiply_matrices

Point = Tuple[float, float]
PONTOS_PADRAO: List[Point] = [(-0.25, -0.25), (0.25, -0.25), (0.25, 0.25), (-0.25, 0.25)]


def criar_tela_transformacoes_2d(janela, voltar_callback):
    tela_transformacoes_2d = tk.Frame(janela)
    tela_transformacoes_2d.grid(row=0, column=0, sticky="nsew")

    lbl_transformacoes = tk.Label(tela_transformacoes_2d, text="Transformações 2D", font=("Helvetica", 14))
    lbl_transformacoes.pack(pady=15)

    content_frame = tk.Frame(tela_transformacoes_2d)
    content_frame.pack(fill=tk.BOTH, expand=True)

    sidebar_frame = tk.Frame(content_frame, width=300)
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    options = ["Translação", "Escala", "Rotação", "Reflexão", "Cisalhamento"]

    combo = ttk.Combobox(sidebar_frame, values=options, state="readonly", font=("Helvetica", 12))
    combo.set(options[0])
    combo.pack(pady=(0, 10))

    inputs_frame = tk.Frame(sidebar_frame)
    inputs_frame.pack(fill=tk.X, expand=False)

    pontos_editor = PointsEditor(sidebar_frame, initial_points=PONTOS_PADRAO)
    pontos_editor.pack(fill=tk.X, pady=5)

    def atualizar_pontos():
        try:
            pontos = pontos_editor.get_points()
            if not pontos:
                pontos = PONTOS_PADRAO
            canvas.set_pontos(pontos)
        except ValueError:
            messagebox.showerror("Erro", "Pontos inválidos no editor.")

    btn_atualizar = tk.Button(sidebar_frame, text="Atualizar Pontos", font=("Helvetica", 12), command=atualizar_pontos)
    btn_atualizar.pack(pady=5)

    console_frame = tk.Frame(content_frame)
    console_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    console_label = tk.Label(console_frame, text="Console:", font=("Helvetica", 12))
    console_label.pack(anchor=tk.W)

    console = scrolledtext.ScrolledText(console_frame, width=100, height=8, font=("Courier", 10))
    console.pack(fill=tk.BOTH, expand=True)

    def limpar_console():
        console.delete(1.0, tk.END)

    limpar_console()

    canvas_frame = tk.Frame(content_frame, width=810, height=610)
    canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas = OpenGLCanvas(canvas_frame, width=800, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.set_pontos(PONTOS_PADRAO)

    def atualizar_conteudo(event=None):
        selected = combo.get()
        for widget in inputs_frame.winfo_children():
            widget.destroy()

        limpar_console()

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

            def aplicar():
                try:
                    tx = float(entrada_tx.get())
                    ty = float(entrada_ty.get())
                    pontos = canvas.get_pontos()
                    if not pontos:
                        pontos = PONTOS_PADRAO
                    limpar_console()
                    console.insert(tk.END, f"Translação por Tx={tx}, Ty={ty}\n")
                    console.insert(tk.END, "Matriz de Translação:\n")
                    mat = translation_matrix(tx, ty)
                    console.insert(tk.END, f"[{mat[0][0]} {mat[0][1]} {mat[0][2]}]\n")
                    console.insert(tk.END, f"[{mat[1][0]} {mat[1][1]} {mat[1][2]}]\n")
                    console.insert(tk.END, f"[{mat[2][0]} {mat[2][1]} {mat[2][2]}]\n\n")
                    console.insert(tk.END, "Pontos Originais:\n")
                    for i, (x, y) in enumerate(pontos):
                        console.insert(tk.END, f"P{i+1}: ({x}, {y}) -> ")
                        nx, ny = apply_matrix_point(mat, x, y)
                        console.insert(tk.END, f"({nx}, {ny})\n")
                    pontos_transformados = [(apply_matrix_point(mat, x, y)[0], apply_matrix_point(mat, x, y)[1]) for x, y in pontos]
                    canvas.set_pontos(pontos_transformados)
                    console.insert(tk.END, "\nPontos Transformados aplicados ao canvas.\n")
                except ValueError:
                    messagebox.showerror("Erro", "Valores inválidos para Tx ou Ty.")

            btn_aplicar = tk.Button(inputs_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar)
            btn_aplicar.pack(pady=5)

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

            tk.Label(inputs_frame, text="Centro de Escala", font=("Helvetica", 12)).pack(pady=10)
            frame_centro = tk.Frame(inputs_frame)
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
                    sx = float(entrada_sx.get())
                    sy = float(entrada_sy.get())
                    cx = float(entrada_cx.get())
                    cy = float(entrada_cy.get())
                    pontos = canvas.get_pontos()
                    if not pontos:
                        pontos = PONTOS_PADRAO
                    limpar_console()
                    console.insert(tk.END, f"Escala por Sx={sx}, Sy={sy} em centro (Cx={cx}, Cy={cy})\n")
                    console.insert(tk.END, "Construção da Matriz de Escala (T(cx,cy) * S(sx,sy) * T(-cx,-cy)):\n")
                    t1 = translation_matrix(-cx, -cy)
                    console.insert(tk.END, "T(-cx,-cy):\n")
                    console.insert(tk.END, f"[{t1[0][0]} {t1[0][1]} {t1[0][2]}]\n")
                    console.insert(tk.END, f"[{t1[1][0]} {t1[1][1]} {t1[1][2]}]\n")
                    console.insert(tk.END, f"[{t1[2][0]} {t1[2][1]} {t1[2][2]}]\n\n")
                    s = [[sx, 0.0, 0.0], [0.0, sy, 0.0], [0.0, 0.0, 1.0]]
                    console.insert(tk.END, "S(sx,sy):\n")
                    console.insert(tk.END, f"[{s[0][0]} {s[0][1]} {s[0][2]}]\n")
                    console.insert(tk.END, f"[{s[1][0]} {s[1][1]} {s[1][2]}]\n")
                    console.insert(tk.END, f"[{s[2][0]} {s[2][1]} {s[2][2]}]\n\n")
                    ts1 = multiply_matrices(s, t1)
                    console.insert(tk.END, "S * T(-cx,-cy):\n")
                    console.insert(tk.END, f"[{ts1[0][0]} {ts1[0][1]} {ts1[0][2]}]\n")
                    console.insert(tk.END, f"[{ts1[1][0]} {ts1[1][1]} {ts1[1][2]}]\n")
                    console.insert(tk.END, f"[{ts1[2][0]} {ts1[2][1]} {ts1[2][2]}]\n\n")
                    t2 = translation_matrix(cx, cy)
                    console.insert(tk.END, "T(cx,cy):\n")
                    console.insert(tk.END, f"[{t2[0][0]} {t2[0][1]} {t2[0][2]}]\n")
                    console.insert(tk.END, f"[{t2[1][0]} {t2[1][1]} {t2[1][2]}]\n")
                    console.insert(tk.END, f"[{t2[2][0]} {t2[2][1]} {t2[2][2]}]\n\n")
                    mat = multiply_matrices(t2, ts1)
                    console.insert(tk.END, "Matriz Final de Escala:\n")
                    console.insert(tk.END, f"[{mat[0][0]} {mat[0][1]} {mat[0][2]}]\n")
                    console.insert(tk.END, f"[{mat[1][0]} {mat[1][1]} {mat[1][2]}]\n")
                    console.insert(tk.END, f"[{mat[2][0]} {mat[2][1]} {mat[2][2]}]\n\n")
                    console.insert(tk.END, "Pontos Originais:\n")
                    for i, (x, y) in enumerate(pontos):
                        console.insert(tk.END, f"P{i+1}: ({x}, {y}) -> ")
                        nx, ny = apply_matrix_point(mat, x, y)
                        console.insert(tk.END, f"({nx}, {ny})\n")
                    pontos_transformados = [(apply_matrix_point(mat, x, y)[0], apply_matrix_point(mat, x, y)[1]) for x, y in pontos]
                    canvas.set_pontos(pontos_transformados)
                    console.insert(tk.END, "\nPontos Transformados aplicados ao canvas.\n")
                except ValueError:
                    messagebox.showerror("Erro", "Valores inválidos.")

            btn_aplicar = tk.Button(inputs_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar)
            btn_aplicar.pack(pady=5)

        elif selected == "Cisalhamento":
            tk.Label(inputs_frame, text="Parâmetros de Cisalhamento", font=("Helvetica", 14)).pack(pady=10)

            frame_shx = tk.Frame(inputs_frame)
            frame_shx.pack(pady=5)
            tk.Label(frame_shx, text="ShX:", font=("Helvetica", 12)).grid(row=0, column=0)
            entrada_shx = tk.Entry(frame_shx, width=10, font=("Helvetica", 12))
            entrada_shx.insert(0, "0.0")
            entrada_shx.grid(row=0, column=1, padx=10)

            frame_shy = tk.Frame(inputs_frame)
            frame_shy.pack(pady=5)
            tk.Label(frame_shy, text="ShY:", font=("Helvetica", 12)).grid(row=0, column=0)
            entrada_shy = tk.Entry(frame_shy, width=10, font=("Helvetica", 12))
            entrada_shy.insert(0, "0.0")
            entrada_shy.grid(row=0, column=1, padx=10)

            tk.Label(inputs_frame, text="Centro de Cisalhamento", font=("Helvetica", 12)).pack(pady=10)
            frame_centro = tk.Frame(inputs_frame)
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
                    shx = float(entrada_shx.get())
                    shy = float(entrada_shy.get())
                    cx = float(entrada_cx.get())
                    cy = float(entrada_cy.get())
                    pontos = canvas.get_pontos() or PONTOS_PADRAO

                    limpar_console()
                    console.insert(tk.END, f"Cisalhamento por ShX={shx}, ShY={shy} em centro (Cx={cx}, Cy={cy})\n")
                    console.insert(tk.END, "Construção da Matriz de Cisalhamento (T(cx,cy) * Sh(shx,shy) * T(-cx,-cy)):\n")

                    t1 = translation_matrix(-cx, -cy)
                    console.insert(tk.END, "T(-cx,-cy):\n")
                    for linha in t1:
                        console.insert(tk.END, f"[{' '.join(map(str, linha))}]\n")
                    console.insert(tk.END, "\n")

                    sh = [[1.0, shx, 0.0],
                        [shy, 1.0, 0.0],
                        [0.0, 0.0, 1.0]]
                    console.insert(tk.END, "Sh(shx,shy):\n")
                    for linha in sh:
                        console.insert(tk.END, f"[{' '.join(map(str, linha))}]\n")
                    console.insert(tk.END, "\n")

                    sh_t1 = multiply_matrices(sh, t1)
                    console.insert(tk.END, "Sh * T(-cx,-cy):\n")
                    for linha in sh_t1:
                        console.insert(tk.END, f"[{' '.join(map(str, linha))}]\n")
                    console.insert(tk.END, "\n")

                    t2 = translation_matrix(cx, cy)
                    console.insert(tk.END, "T(cx,cy):\n")
                    for linha in t2:
                        console.insert(tk.END, f"[{' '.join(map(str, linha))}]\n")
                    console.insert(tk.END, "\n")

                    mat = multiply_matrices(t2, sh_t1)
                    console.insert(tk.END, "Matriz Final de Cisalhamento:\n")
                    for linha in mat:
                        console.insert(tk.END, f"[{' '.join(map(str, linha))}]\n")
                    console.insert(tk.END, "\n")

                    console.insert(tk.END, "Pontos Originais -> Transformados:\n")
                    pontos_transformados = []
                    for i, (x, y) in enumerate(pontos):
                        nx, ny = apply_matrix_point(mat, x, y)
                        pontos_transformados.append((nx, ny))
                        console.insert(tk.END, f"P{i+1}: ({x}, {y}) -> ({nx}, {ny})\n")

                    canvas.set_pontos(pontos_transformados)
                    console.insert(tk.END, "\nPontos transformados aplicados ao canvas.\n")

                except ValueError:
                    messagebox.showerror("Erro", "Valores inválidos para ShX, ShY, Cx ou Cy.")


            btn_aplicar = tk.Button(inputs_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar)
            btn_aplicar.pack(pady=5)

        elif selected == "Rotação":
            #view
            TRIANGLE = [(0.0, 0.0),(0.4, 0.0),(0.2, 0.4)]
            pontos_editor.set_points(TRIANGLE)
            canvas.set_pontos(pontos_editor.get_points())
            
            tk.Label(inputs_frame, text="Parâmetros da Rotação", font=("Helvetica", 14)).pack(pady=10)

            frame_angle = tk.Frame(inputs_frame)
            frame_angle.pack(pady=5)
            tk.Label(frame_angle, text="Angulo:", font=("Helvetica", 12)).grid(row=0, column=0)
            entrada_angle = tk.Entry(frame_angle, width=10, font=("Helvetica", 12))
            entrada_angle.insert(0, "0.0")
            entrada_angle.grid(row=0, column=1, padx=10)

            #controller
            def aplicar():
                try:
                    angle = float(entrada_angle.get())
                    pontos = CGMatriz.create_by_pointlist(pontos_editor.get_points())

                    limpar_console()
                    console.insert(tk.END, f"Rotação em '{angle}' graus)\n")
                    console.insert(tk.END, f"Matriz dos Pontos:\n")
                    console.insert(tk.END, f"{pontos}\n\n")

                    matriz_de_rotacao = CGMatriz.get_rotate(angle)
                    pontos = pontos * matriz_de_rotacao
                    
                    console.insert(tk.END, f"Matriz de Rotação em '{angle}' graus:\n")
                    console.insert(tk.END, f"{matriz_de_rotacao}\n\n")

                    canvas.set_pontos(pontos.to_points())
                    pontos_editor.set_points(pontos.to_points())

                    console.insert(tk.END, f"Matriz Resultante:\n")
                    console.insert(tk.END, f"{pontos}\n")

                except ValueError:
                    messagebox.showerror("Erro", "Valores inválidos para ShX, ShY, Cx ou Cy.")

            btn_aplicar = tk.Button(inputs_frame, text="Aplicar", font=("Helvetica", 12), command=aplicar)
            btn_aplicar.pack(pady=5)


        else:
            tk.Label(inputs_frame, text=f"{selected} em desenvolvimento", font=("Helvetica", 12)).pack(expand=True)

    combo.bind("<<ComboboxSelected>>", atualizar_conteudo)

    atualizar_conteudo()

    btn_voltar_transformacoes = tk.Button(
        tela_transformacoes_2d,
        text="Voltar",
        width=10,
        command=voltar_callback,
    )
    btn_voltar_transformacoes.pack(pady=20)

    return tela_transformacoes_2d
