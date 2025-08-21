import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services.calculo_setPixel import setPixel 

def criar_tela_setpixel(root, voltar_callback):
    root.geometry("1000x700")

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="SetPixel", font=("Helvetica", 20)).pack(pady=20)

    frame_cenario = tk.Frame(root)
    frame_cenario.pack(pady=10)
    tk.Label(frame_cenario, text="Selecione o cenário:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
    opcoes = ["[-1, 1]", "[0, 1]"]
    combo_cenario = ttk.Combobox(frame_cenario, values=opcoes, state="readonly", width=15, font=("Helvetica", 11))
    combo_cenario.set(opcoes[0])
    combo_cenario.grid(row=0, column=1)

    frame_tamanho = tk.Frame(root)
    frame_tamanho.pack(pady=10)
    tk.Label(frame_tamanho, text="Tamanho da tela:", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=4)
    tk.Label(frame_tamanho, text="Largura:", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e")
    entrada_largura = tk.Entry(frame_tamanho, width=10, font=("Helvetica", 11))
    entrada_largura.insert(0, "800")
    entrada_largura.grid(row=1, column=1, padx=10)
    tk.Label(frame_tamanho, text="Altura:", font=("Helvetica", 11)).grid(row=1, column=2, sticky="e")
    entrada_altura = tk.Entry(frame_tamanho, width=10, font=("Helvetica", 11))
    entrada_altura.insert(0, "400")
    entrada_altura.grid(row=1, column=3, padx=10)

    frame_coords = tk.Frame(root)
    frame_coords.pack(pady=10)
    tk.Label(frame_coords, text="Coordenadas do ponto:", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=4)
    tk.Label(frame_coords, text="X:", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e")
    entrada_x = tk.Entry(frame_coords, width=10, font=("Helvetica", 11))
    entrada_x.insert(0, "0")
    entrada_x.grid(row=1, column=1, padx=10)
    tk.Label(frame_coords, text="Y:", font=("Helvetica", 11)).grid(row=1, column=2, sticky="e")
    entrada_y = tk.Entry(frame_coords, width=10, font=("Helvetica", 11))
    entrada_y.insert(0, "0")
    entrada_y.grid(row=1, column=3, padx=10)

    frame_limites = tk.Frame(root)
    frame_limites.pack(pady=10)
    tk.Label(frame_limites, text="Limites do plano (mínimos e máximos):", font=("Helvetica", 12)).grid(row=0, column=0, columnspan=4)
    tk.Label(frame_limites, text="Xmin:", font=("Helvetica", 11)).grid(row=1, column=0, sticky="e")
    entrada_xmin = tk.Entry(frame_limites, width=10, font=("Helvetica", 11))
    entrada_xmin.insert(0, "10.5")
    entrada_xmin.grid(row=1, column=1, padx=10)
    tk.Label(frame_limites, text="Xmax:", font=("Helvetica", 11)).grid(row=1, column=2, sticky="e")
    entrada_xmax = tk.Entry(frame_limites, width=10, font=("Helvetica", 11))
    entrada_xmax.insert(0, "100.3")
    entrada_xmax.grid(row=1, column=3, padx=10)
    tk.Label(frame_limites, text="Ymin:", font=("Helvetica", 11)).grid(row=2, column=0, sticky="e")
    entrada_ymin = tk.Entry(frame_limites, width=10, font=("Helvetica", 11))
    entrada_ymin.insert(0, "10.5")
    entrada_ymin.grid(row=2, column=1, padx=10)
    tk.Label(frame_limites, text="Ymax:", font=("Helvetica", 11)).grid(row=2, column=2, sticky="e")
    entrada_ymax = tk.Entry(frame_limites, width=10, font=("Helvetica", 11))
    entrada_ymax.insert(0, "100.3")
    entrada_ymax.grid(row=2, column=3, padx=10)

    def ao_clicar_desenhar():
        try:
            cenario_selecionado = combo_cenario.get()
            valor_cenario = 0 
            if cenario_selecionado == "[-1, 1]":
                valor_cenario = 1
            elif cenario_selecionado == "[0, 1]":
                valor_cenario = 0
            x = float(entrada_x.get())
            y = float(entrada_y.get())
            xmin = float(entrada_xmin.get())
            xmax = float(entrada_xmax.get())
            ymin = float(entrada_ymin.get())
            ymax = float(entrada_ymax.get())

            if not (xmin <= x <= xmax):
                messagebox.showerror("Erro", f"X = {x} está fora dos limites [{xmin}, {xmax}]")
                return
            if not (ymin <= y <= ymax):
                messagebox.showerror("Erro", f"Y = {y} está fora dos limites [{ymin}, {ymax}]")
                return

            messagebox.showinfo("Sucesso", "Coordenada válida dentro dos limites definidos.")
            
            string_com_calculos = setPixel(xmin, ymin, xmax, ymax, x, y, int(entrada_largura.get()), int(entrada_altura.get()), valor_cenario)

            texto_resultados.config(state='normal')
            texto_resultados.delete('1.0', tk.END)
            texto_resultados.insert(tk.END, string_com_calculos)
            texto_resultados.config(state='disabled')

        except ValueError:
            messagebox.showerror("Erro", "Insira apenas valores numéricos.")

    botao_desenhar = tk.Button(root, text="Desenhar", width=20, height=2, font=("Helvetica", 12), command=ao_clicar_desenhar)
    botao_desenhar.pack(pady=20)

    botao_voltar = tk.Button(root, text="Voltar", width=20, height=2, font=("Helvetica", 12), command=voltar_callback)
    botao_voltar.pack(pady=10)

    frame_resultados = tk.Frame(root, relief=tk.SUNKEN, borderwidth=1)
    frame_resultados.pack(fill="both", expand=True, padx=20, pady=10)

    tk.Label(frame_resultados, text="Resultados do Cálculo", font=("Helvetica", 13, "bold")).pack(pady=(5,0))
    

    scrollbar = tk.Scrollbar(frame_resultados)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,5), pady=5)

    texto_resultados = tk.Text(
        frame_resultados, 
        height=10, 
        font=("Courier New", 11), 
        wrap=tk.WORD, 
        yscrollcommand=scrollbar.set,
    )
    texto_resultados.pack(pady=5, padx=(5,0), fill="both", expand=True)

    scrollbar.config(command=texto_resultados.yview)

    texto_ficticio = (
        "Função SetPixel\n\n"
    )
    texto_resultados.insert(tk.END, texto_ficticio)
    texto_resultados.config(state='disabled')