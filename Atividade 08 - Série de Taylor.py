import tkinter as tk
from tkinter import ttk, messagebox
import math

# --- Paleta de Cores e Fontes NEON ---
COR_FUNDO = "#010101"          # Preto profundo
COR_NEON_CYAN = "#00FFFF"      # Ciano brilhante para títulos e destaques
COR_NEON_LIMA = "#39FF14"      # Verde-limão para botões e resultados
COR_TEXTO = "#F0F0F0"          # Branco suave para textos comuns

FONTE_PRINCIPAL = ("Consolas", 16, "bold")
FONTE_TITULO = ("Consolas", 12, "bold")
FONTE_TEXTO = ("Consolas", 10)
FONTE_RESULTADO = ("Consolas", 11, "bold")

# --- Lógica de Cálculo (Inalterada) ---
def calcular_ln_taylor(x, erro_max):
    if x <= -1 or x > 1:
        return None, 0
    soma_aproximada = 0
    termo_atual = x
    n = 1
    max_iteracoes = 1000
    while abs(termo_atual) > erro_max and n <= max_iteracoes:
        soma_aproximada += termo_atual
        sinal = (-1)**n
        n += 1
        termo_atual = sinal * (x**n) / n
    if n > max_iteracoes:
        return float('inf'), n-1
    return soma_aproximada, n - 1

# --- Funções da Interface ---
def executar_calculo_ln1_5():
    try:
        x = 0.5
        erro_desejado = 10**(-4)
        valor_aprox, termos = calcular_ln_taylor(x, erro_desejado)
        valor_exato = math.log(1 + x)
        resultado_aprox_var.set(f"{valor_aprox:.6f}")
        resultado_exato_var.set(f"{valor_exato:.6f}")
        resultado_termos_var.set(f"{termos} termos")
    except Exception as e:
        messagebox.showerror("Erro no Sistema", f"Falha na matriz de cálculo: {e}")

# --- Configuração da Janela Principal ---
janela = tk.Tk()
janela.title("»> Interface de Análise Quântica | Série de Taylor «<")
janela.geometry("600x550")
janela.configure(bg=COR_FUNDO)
janela.resizable(False, False)

# --- Configuração de Estilo (O coração do design) ---
style = ttk.Style(janela)
# O tema 'clam' é mais fácil de customizar que o padrão
style.theme_use('clam')

# Estilo para os Frames
style.configure('TFrame', background=COR_FUNDO)

# Estilo para os LabelFrames (Contêineres com título)
style.configure('TLabelframe',
                background=COR_FUNDO,
                bordercolor=COR_NEON_CYAN,
                relief="solid")
style.configure('TLabelframe.Label',
                background=COR_FUNDO,
                foreground=COR_NEON_CYAN,
                font=FONTE_TITULO)

# Estilo para Labels comuns
style.configure('TLabel',
                background=COR_FUNDO,
                foreground=COR_TEXTO,
                font=FONTE_TEXTO)

# Estilo para o botão NEON
style.configure('Neon.TButton',
                font=FONTE_TITULO,
                background=COR_NEON_LIMA,
                foreground=COR_FUNDO,
                borderwidth=0,
                focusthickness=0, # Remove a linha pontilhada de foco
                relief='flat')
# Efeito de hover (mouse em cima)
style.map('Neon.TButton',
          background=[('active', COR_FUNDO)],
          foreground=[('active', COR_NEON_LIMA)])

# --- Widgets da Interface ---

# Título Principal
lbl_titulo_main = ttk.Label(janela, text="SISTEMA DE ANÁLISE DE SÉRIE",
                            font=FONTE_PRINCIPAL,
                            foreground=COR_NEON_CYAN)
lbl_titulo_main.pack(pady=(20, 10))

# --- Seção para ln(1.5) ---
frame_ln1_5 = ttk.LabelFrame(janela, text=" MÓDULO DE CÁLCULO: ln(1.5) ")
frame_ln1_5.pack(fill="x", padx=20, pady=10)

ttk.Label(frame_ln1_5, text="Pressione para iniciar a computação com erro < 10⁻⁴:", anchor="center").pack(pady=5, fill="x")

btn_calcular = ttk.Button(frame_ln1_5, text="» COMPILAR «", style="Neon.TButton", command=executar_calculo_ln1_5, cursor="hand2")
btn_calcular.pack(pady=(10, 20), ipady=5, ipadx=10)

# Grid para exibir os resultados
frame_resultados = ttk.Frame(frame_ln1_5)
frame_resultados.pack(pady=5, padx=20)

resultado_aprox_var = tk.StringVar(value="--")
resultado_exato_var = tk.StringVar(value="--")
resultado_termos_var = tk.StringVar(value="--")

ttk.Label(frame_resultados, text="Valor Compilado (Taylor):").grid(row=0, column=0, sticky="e", padx=10)
lbl_res_aprox = ttk.Label(frame_resultados, textvariable=resultado_aprox_var, font=FONTE_RESULTADO, foreground=COR_NEON_LIMA)
lbl_res_aprox.grid(row=0, column=1, sticky="w")

ttk.Label(frame_resultados, text="Valor Real (Referência):").grid(row=1, column=0, sticky="e", padx=10)
lbl_res_exato = ttk.Label(frame_resultados, textvariable=resultado_exato_var, font=FONTE_RESULTADO, foreground=COR_NEON_LIMA)
lbl_res_exato.grid(row=1, column=1, sticky="w")

ttk.Label(frame_resultados, text="Iterações Necessárias:").grid(row=2, column=0, sticky="e", padx=10)
lbl_res_termos = ttk.Label(frame_resultados, textvariable=resultado_termos_var, font=FONTE_RESULTADO, foreground=COR_NEON_LIMA)
lbl_res_termos.grid(row=2, column=1, sticky="w")


# --- Seção para Explicação de ln(2.71828) ---
frame_ln2_7 = ttk.LabelFrame(janela, text=" ALERTA DE DIVERGÊNCIA: ln(2.71828) ")
frame_ln2_7.pack(fill="both", expand=True, padx=20, pady=10)

texto_explicacao = """
A simulação para ln(1+x) com x = 1.71828 falha.

MOTIVO: O raio de convergência da série de Taylor para ln(1+x) é estritamente no intervalo -1 < x ≤ 1.

O valor x = 1.71828 viola este protocolo. A série diverge, gerando uma cascata de dados infinita em vez de convergir para o valor real. A integridade do sistema não pode ser garantida fora dos parâmetros de convergência.
"""

# Widget de Texto estilizado para parecer um terminal
text_widget = tk.Text(frame_ln2_7,
                      wrap="word",
                      bg=COR_FUNDO,
                      fg=COR_TEXTO,
                      font=FONTE_TEXTO,
                      borderwidth=1,
                      relief="solid",
                      highlightbackground=COR_NEON_CYAN, # Cor da borda quando não está em foco
                      highlightcolor=COR_NEON_CYAN,      # Cor da borda quando em foco
                      highlightthickness=1,
                      insertbackground=COR_TEXTO) # Cor do cursor de texto
text_widget.insert("1.0", texto_explicacao)
text_widget.config(state="disabled")
text_widget.pack(expand=True, fill="both", padx=10, pady=10)

# --- Inicia a Interface ---
janela.mainloop()