import tkinter as tk
from tkinter import messagebox
import random
import threading
import time

# Variáveis globais
numero_secreto = 0
tentativas_restantes = 0
pontuacao = 0
timer_segundos = 0
timer_ativo = False  # controle para o timer

# Função para iniciar o jogo
def iniciar_jogo(dificuldade):
    global numero_secreto, tentativas_restantes, timer_segundos, timer_ativo

    if dificuldade == "Fácil":
        numero_secreto = random.randint(1, 10)
        tentativas_restantes = 5
        timer_segundos = 30
        margem = "1 a 10"
    elif dificuldade == "Médio":
        numero_secreto = random.randint(1, 100)
        tentativas_restantes = 7
        timer_segundos = 60
        margem = "1 a 100"
    elif dificuldade == "Difícil":
        numero_secreto = random.randint(1, 1000)
        tentativas_restantes = 10
        timer_segundos = 90
        margem = "1 a 1000"

    label_dificuldade.config(text=f"Dificuldade: {dificuldade} (número entre {margem})")
    label_tentativas.config(text=f"Tentativas restantes: {tentativas_restantes}")
    entrada_numero.delete(0, tk.END)

    timer_ativo = True  # Ativando o controle do timer
    iniciar_timer()

# Função para verificar o palpite
def verificar_palpite():
    global tentativas_restantes, pontuacao, timer_ativo

    try:
        palpite = int(entrada_numero.get())
    except ValueError:
        messagebox.showwarning("Erro", "Por favor, insira um número válido!")
        return

    entrada_numero.delete(0, tk.END)
    tentativas_restantes -= 1
    label_tentativas.config(text=f"Tentativas restantes: {tentativas_restantes}")

    if palpite == numero_secreto:
        timer_ativo = False  # Desativa o timer
        pontos_ganhos = tentativas_restantes * 10
        pontuacao += pontos_ganhos
        messagebox.showinfo("Parabéns!", f"Você acertou! Pontos ganhos: {pontos_ganhos}")
        reiniciar_jogo()
    elif tentativas_restantes == 0:
        timer_ativo = False  # Desativa o timer
        messagebox.showinfo("Fim de Jogo", f"Você perdeu! O número era {numero_secreto}.")
        reiniciar_jogo()
    elif palpite < numero_secreto:
        messagebox.showinfo("Dica", "Tente algo maior")
    else:
        messagebox.showinfo("Dica", "Tente algo menor")
    
    label_pontuacao.config(text=f"Pontuação: {pontuacao}")

# Função para reiniciar o jogo
def reiniciar_jogo():
    global timer_ativo
    entrada_numero.delete(0, tk.END)
    label_dificuldade.config(text="Escolha uma dificuldade para começar!")
    label_tentativas.config(text="")
    label_timer.config(text="")
    timer_ativo = False  # Garante que o timer é desativado

def iniciar_timer():
    global timer_segundos, timer_ativo

    def atualizar_timer():
        global timer_segundos, timer_ativo  # Declarar ambas as variáveis como globais
        if timer_ativo and timer_segundos > 0:
            label_timer.config(text=f"Tempo restante: {timer_segundos}s")
            timer_segundos -= 1
            janela.after(1000, atualizar_timer)  # Chama a função novamente após 1 segundo
        elif timer_ativo and timer_segundos == 0:
            timer_ativo = False  # Desativa o timer
            messagebox.showinfo("Tempo Esgotado", "Acabou o tempo!")
            reiniciar_jogo()

    atualizar_timer()  # Inicia o timer


# Função para aplicar tema
def aplicar_tema(tema):
    if tema == "Futurista":
        janela.config(bg="black")
        label_dificuldade.config(fg="white", bg="black")
        label_tentativas.config(fg="cyan", bg="black")
        label_timer.config(fg="red", bg="black")
        label_pontuacao.config(fg="lime", bg="black")
    elif tema == "Colorido":
        janela.config(bg="pink")
        label_dificuldade.config(fg="purple", bg="yellow")
        label_tentativas.config(fg="blue", bg="orange")
        label_timer.config(fg="green", bg="pink")
        label_pontuacao.config(fg="blue", bg="pink")

# Criação da janela principal
janela = tk.Tk()
janela.title("Jogo de Adivinhação")
janela.geometry("500x400")

# Widgets da interface
label_dificuldade = tk.Label(janela, text="Escolha uma dificuldade para começar!", font=("Arial", 14))
label_dificuldade.pack(pady=10)

label_tentativas = tk.Label(janela, text="", font=("Arial", 12))
label_tentativas.pack(pady=5)

label_timer = tk.Label(janela, text="", font=("Arial", 12))
label_timer.pack(pady=5)

label_pontuacao = tk.Label(janela, text="Pontuação: 0", font=("Arial", 12))
label_pontuacao.pack(pady=5)

entrada_numero = tk.Entry(janela, font=("Arial", 14))
entrada_numero.pack(pady=10)

botao_verificar = tk.Button(janela, text="Verificar", font=("Arial", 12), command=verificar_palpite)
botao_verificar.pack(pady=10)

frame_dificuldades = tk.Frame(janela)
frame_dificuldades.pack(pady=10)

botao_facil = tk.Button(frame_dificuldades, text="Fácil", font=("Arial", 12), command=lambda: iniciar_jogo("Fácil"))
botao_facil.grid(row=0, column=0, padx=5)

botao_medio = tk.Button(frame_dificuldades, text="Médio", font=("Arial", 12), command=lambda: iniciar_jogo("Médio"))
botao_medio.grid(row=0, column=1, padx=5)

botao_dificil = tk.Button(frame_dificuldades, text="Difícil", font=("Arial", 12), command=lambda: iniciar_jogo("Difícil"))
botao_dificil.grid(row=0, column=2, padx=5)

frame_temas = tk.Frame(janela)
frame_temas.pack(pady=10)

botao_tema_futurista = tk.Button(frame_temas, text="Futurista", font=("Arial", 12), command=lambda: aplicar_tema("Futurista"))
botao_tema_futurista.grid(row=0, column=0, padx=5)

botao_tema_colorido = tk.Button(frame_temas, text="Colorido", font=("Arial", 12), command=lambda: aplicar_tema("Colorido"))
botao_tema_colorido.grid(row=0, column=1, padx=5)

# Loop principal da interface
janela.mainloop()
