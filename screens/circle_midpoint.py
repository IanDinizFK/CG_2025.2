# seu_projeto/screens/criar_tela_circulo.py

import tkinter as tk
from tkinter import ttk, messagebox

from services.circunferencia.circle_midpoint import midpoint_algorithm, desenhar_circulo_opengl as desenhar_midpoint_opengl
from services.circunferencia.polimonial import polynomial_algorithm, desenhar_circulo_opengl as desenhar_poly_opengl
from services.circunferencia.trigonometrico import trigonometric_algorithm, desenhar_circulo_opengl as desenhar_trig_opengl

def criar_tela_circulo(root, voltar_callback):
    root.geometry("600x650")

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Desenho de Círculo", font=("Helvetica", 16)).pack(pady=10)
    
    frame_algoritmo = tk.Frame(root)
    frame_algoritmo.pack(pady=5)
    tk.Label(frame_algoritmo, text="Algoritmo:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
    opcoes_algoritmo = ["Ponto Médio", "Polinomial", "Trigonométrico"]
    combo_algoritmo = ttk.Combobox(frame_algoritmo, values=opcoes_algoritmo, state="readonly", font=("Helvetica", 12))
    combo_algoritmo.set(opcoes_algoritmo[0])
    combo_algoritmo.grid(row=0, column=1)

    frame_entradas = tk.Frame(root)
    frame_entradas.pack(pady=10)
    
    tk.Label(frame_entradas, text="Centro X (xc):", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=2, sticky='w')
    entrada_xc = tk.Entry(frame_entradas, width=10, font=("Helvetica", 12))
    entrada_xc.grid(row=0, column=1, padx=5, pady=2)
    
    tk.Label(frame_entradas, text="Centro Y (yc):", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=2, sticky='w')
    entrada_yc = tk.Entry(frame_entradas, width=10, font=("Helvetica", 12))
    entrada_yc.grid(row=1, column=1, padx=5, pady=2)

    tk.Label(frame_entradas, text="Raio:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5, pady=2, sticky='w')
    entrada_raio = tk.Entry(frame_entradas, width=10, font=("Helvetica", 12))
    entrada_raio.grid(row=2, column=1, padx=5, pady=2)

    tk.Label(frame_entradas, text="Largura Tela:", font=("Helvetica", 12)).grid(row=3, column=0, padx=5, pady=2, sticky='w')
    entrada_largura = tk.Entry(frame_entradas, width=10, font=("Helvetica", 12))
    entrada_largura.grid(row=3, column=1, padx=5, pady=2)
    
    tk.Label(frame_entradas, text="Altura Tela:", font=("Helvetica", 12)).grid(row=4, column=0, padx=5, pady=2, sticky='w')
    entrada_altura = tk.Entry(frame_entradas, width=10, font=("Helvetica", 12))
    entrada_altura.grid(row=4, column=1, padx=5, pady=2)

    entrada_largura.insert(0, "800")
    entrada_altura.insert(0, "600")
    entrada_xc.insert(0, "400")
    entrada_yc.insert(0, "300")
    entrada_raio.insert(0, "150")

    def ao_clicar_desenhar():
        try:
            raio = int(entrada_raio.get())
            largura = int(entrada_largura.get())
            altura = int(entrada_altura.get())
            xc = int(entrada_xc.get())
            yc = int(entrada_yc.get())
            algoritmo_selecionado = combo_algoritmo.get()
            
            yc_gl = altura - yc

            if raio <= 0:
                messagebox.showerror("Erro", "O raio deve ser maior que 0.")
                return

            pontos, calculo_str = None, ""

            if algoritmo_selecionado == "Ponto Médio":
                pontos, calculo_str = midpoint_algorithm(raio)
                texto_resultados.config(state='normal')
                texto_resultados.delete('1.0', tk.END)
                texto_resultados.insert(tk.END, f"--- Algoritmo do Ponto Médio ---\n\n{calculo_str}")
                texto_resultados.config(state='disabled')
                desenhar_midpoint_opengl(largura, altura, xc, yc_gl, pontos)

            elif algoritmo_selecionado == "Polinomial":
                pontos, calculo_str = polynomial_algorithm(raio)
                texto_resultados.config(state='normal')
                texto_resultados.delete('1.0', tk.END)
                texto_resultados.insert(tk.END, f"--- Algoritmo Polinomial ---\n\n{calculo_str}")
                texto_resultados.config(state='disabled')
                desenhar_poly_opengl(largura, altura, xc, yc_gl, pontos)

            elif algoritmo_selecionado == "Trigonométrico":
                pontos, calculo_str = trigonometric_algorithm(raio)
                texto_resultados.config(state='normal')
                texto_resultados.delete('1.0', tk.END)
                texto_resultados.insert(tk.END, f"--- Algoritmo Trigonométrico ---\n\n{calculo_str}")
                texto_resultados.config(state='disabled')
                desenhar_trig_opengl(largura, altura, xc, yc_gl, pontos)

        except ValueError:
            messagebox.showerror("Erro", "Digite valores numéricos válidos para todas as entradas.")

    tk.Button(root, text="Desenhar", width=20, height=2, font=("Helvetica", 12), command=ao_clicar_desenhar).pack(pady=15)

    # --- Telinha de Cálculos (sem alterações) ---
    frame_resultados = tk.Frame(root, relief=tk.SUNKEN, borderwidth=1)
    frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)
    tk.Label(frame_resultados, text="Passos do Cálculo", font=("Helvetica", 13, "bold")).pack(pady=(5,0))
    scrollbar = tk.Scrollbar(frame_resultados)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,5), pady=5)
    texto_resultados = tk.Text(
        frame_resultados, height=10, font=("Courier New", 10), 
        wrap=tk.WORD, yscrollcommand=scrollbar.set
    )
    texto_resultados.pack(pady=5, padx=(5,0), fill="both", expand=True)
    scrollbar.config(command=texto_resultados.yview)
    texto_resultados.insert(tk.END, "Os passos do cálculo aparecerão aqui após clicar em 'Desenhar'.")
    texto_resultados.config(state='disabled')

    tk.Button(root, text="Voltar", width=20, height=2, font=("Helvetica", 12), command=voltar_callback).pack(pady=10)