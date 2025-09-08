import tkinter as tk
from tkinter import messagebox
from services.circle_midpoint import desenhar_circulo_opengl

def criar_tela_circulo(root, voltar_callback):
    root.geometry("600x400")

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Algoritmo do Círculo (Ponto Médio)", font=("Helvetica", 16)).pack(pady=20)

    frame_raio = tk.Frame(root)
    frame_raio.pack(pady=10)

    tk.Label(frame_raio, text="Raio:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
    entrada_raio = tk.Entry(frame_raio, width=10, font=("Helvetica", 12))
    entrada_raio.insert(0, "50")
    entrada_raio.grid(row=0, column=1)

    frame_tamanho = tk.Frame(root)
    frame_tamanho.pack(pady=10)

    tk.Label(frame_tamanho, text="Largura:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
    entrada_largura = tk.Entry(frame_tamanho, width=10, font=("Helvetica", 12))
    entrada_largura.insert(0, "800")
    entrada_largura.grid(row=0, column=1)

    tk.Label(frame_tamanho, text="Altura:", font=("Helvetica", 12)).grid(row=0, column=2, padx=5)
    entrada_altura = tk.Entry(frame_tamanho, width=10, font=("Helvetica", 12))
    entrada_altura.insert(0, "600")
    entrada_altura.grid(row=0, column=3)

    def ao_clicar_desenhar():
        try:
            raio = int(entrada_raio.get())
            largura = int(entrada_largura.get())
            altura = int(entrada_altura.get())

            if raio <= 0:
                messagebox.showerror("Erro", "Raio deve ser maior que 0.")
                return

            desenhar_circulo_opengl(largura, altura, raio)

        except ValueError:
            messagebox.showerror("Erro", "Digite valores numéricos válidos.")

    tk.Button(root, text="Desenhar", width=20, height=2, font=("Helvetica", 12), command=ao_clicar_desenhar).pack(pady=20)

    tk.Button(root, text="Voltar", width=20, height=2, font=("Helvetica", 12), command=voltar_callback).pack(pady=10)
