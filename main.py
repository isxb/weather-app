import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from datetime import datetime
import pytz
import pycountry_convert as pc

# Configurações iniciais
API_KEY = "" #COLOQUE SUA CHAVE API PARA FUNCIONAR (https://openweathermap.org/)
cidade = 'pesquisa_local'

# Cores
co0 = "#444466"
co1 = "#feffff"
co2 = "#000000"
fundo_dia = "#6cc4cc"
fundo_noite = "#484f60"
fundo_tarde = "#bfb86d"
fundo = fundo_dia

# Janela principal
janela = tk.Tk()
janela.title("Previsão do Tempo")
janela.geometry("350x400")
janela.configure(bg=fundo)

ttk.Separator(janela, orient=tk.HORIZONTAL).grid(row=0, columnspan=1, ipadx=174)

#FRAMES
frame_top = tk.Frame(janela, width=350, height=50, bg=co1, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = tk.Frame(janela, width=350, height=350, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=tk.NW)

#FRAME PARA LISTA DE CIDADES (AUTOCOMPLETAR)
frame_lista = tk.Frame(janela, bg=co1)
frame_lista.place(x=15, y=50, width=320, height=100)
frame_lista.place_forget()

# LISTA DE CIDADES
lista_cidades = tk.Listbox(frame_lista, width=40, height=4, bg=co1, fg=co0, font=("Arial", 10))
lista_cidades.pack(fill=tk.BOTH, expand=True)

# FUNÇÃO PARA BUSCAR CIDADE 
def buscar_cidades(event=None):
    termo = pesquisa_local.get()
    if len(termo) >= 2:  # SÓ BUSCA SE DIGITAR MAIS DE DOIS CARACTER
        link = f"http://api.openweathermap.org/geo/1.0/direct?q={termo}&limit=5&appid={API_KEY}"
        resposta = requests.get(link)
        if resposta.status_code == 200:
            cidades = resposta.json()
            lista_cidades.delete(0, tk.END) 
            for cidade in cidades:
                nome_cidade = cidade.get('name', '')
                pais = cidade.get('country', '')
                lista_cidades.insert(tk.END, f"{nome_cidade}, {pais}")
            frame_lista.lift() 
            frame_lista.place(x=15, y=50) 
        else:
            lista_cidades.delete(0, tk.END)
            lista_cidades.insert(tk.END, "Erro ao buscar cidades.")
    else:
        frame_lista.place_forget()

#FUNÇÃO PARA SELECIONAR CIDADE

def selecionar_cidade(event):
    selecionado = lista_cidades.get(tk.ACTIVE)
    if selecionado:
        cidade = selecionado.split(",")[0]
        pesquisa_local.delete(0, tk.END)
        pesquisa_local.insert(0, cidade)
        frame_lista.place_forget()

#FUNÇÃO PARA AJUSTAR CORES DO FUNDO
def ajustar_cores_texto(fundo):
    if fundo in [fundo_noite, fundo_tarde]:
        cor_texto = co1
    else:
        cor_texto = co2

    # APLICAR COR AOS TEXTOS
    cidade_lab.config(fg=cor_texto)
    data_lab.config(fg=cor_texto)
    temperatura_lab.config(fg=cor_texto)
    sensacao_lab.config(fg=cor_texto)
    pressao_lab.config(fg=cor_texto)
    humidade_lab.config(fg=cor_texto)
    vento_lab.config(fg=cor_texto)
    descricao_lab.config(fg=cor_texto)

# FUNÇÃO PARA OBTER INFORMAÇÕES DO CLIMA
def informacao():
    cidade = pesquisa_local.get()
    link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    resposta = requests.get(link)

    if resposta.status_code == 200:
        dados = resposta.json()

        # INFORMAÇÕES DO PAIS E HORARIO
        pais_codigo = dados['sys']['country']
        zona_fuso = pytz.country_timezones[pais_codigo]
        pais = pytz.country_names[pais_codigo]

        # DATA E HORA LOCAL
        data_zona = pytz.timezone(zona_fuso[0])
        hora_zona = datetime.now(data_zona).strftime("%d/%m/%Y | %I:%M:%S %p")

        # INFORMAÇÕES CLIMA
        temperatura = dados['main']['temp']
        sensacao = dados['main']['feels_like']
        pressao = dados['main']['pressure']
        humidade = dados['main']['humidity']
        vento = dados['wind']['speed']
        descricao_clima = dados['weather'][0]['description']


        def pais_para_continente(i):
            pais_alpha = pc.country_name_to_country_alpha2(i)
            pais_continent_codigo = pc.country_alpha2_to_continent_code(pais_alpha)
            return pc.convert_continent_code_to_continent_name(pais_continent_codigo)

        continente = pais_para_continente(pais)

        # Atualizar labels
        cidade_lab['text'] = f"{cidade} - {pais} / {continente}"
        data_lab['text'] = hora_zona
        temperatura_lab['text'] = f"{temperatura:.1f}°C"
        sensacao_lab['text'] = f"Sensação: {sensacao:.1f}°C"
        pressao_lab['text'] = f"Pressão: {pressao} hPa"
        humidade_lab['text'] = f"Humidade: {humidade}%"
        vento_lab['text'] = f"Vento: {vento} m/s"
        descricao_lab['text'] = descricao_clima.capitalize()

        # LOGICA PARA MUDANÇA DE ICONE FUNDO
        zona_periodo = datetime.now(data_zona).strftime('%H')
        zona_periodo = int(zona_periodo)

        global fundo, imagem


        if 18 <= zona_periodo or zona_periodo <= 5:
            fundo = fundo_noite
            try:
                imagem = Image.open('image/lua.png')
            except FileNotFoundError:
                print("Erro: Imagem 'lua.png' não encontrada.")
                imagem = None
        elif 6 <= zona_periodo <= 11:
            fundo = fundo_dia
            try:
                imagem = Image.open('image/ensolarado.png')  
            except FileNotFoundError:
                print("Erro: Imagem 'ensolarado.png' não encontrada.")
                imagem = None
        elif 12 <= zona_periodo <= 17:
            fundo = fundo_tarde
            try:
                imagem = Image.open('image/tarde.png')  
            except FileNotFoundError:
                print("Erro: Imagem 'tarde.png' não encontrada.")
                imagem = None

        if 'nublado' in descricao_clima.lower():
            try:
                imagem = Image.open('image/nublado.png') 
            except FileNotFoundError:
                print("Erro: Imagem 'nublado.png' não encontrada.")
                imagem = None
        elif 'parcialmente nublado' in descricao_clima.lower():
            try:
                imagem = Image.open('image/parcialmente_nublado.png')
            except FileNotFoundError:
                print("Erro: Imagem 'parcialmente_nublado.png' não encontrada.")
                imagem = None
        elif 'chuva' in descricao_clima.lower():
            try:
                imagem = Image.open('image/chuvoso.png') 
            except FileNotFoundError:
                print("Erro: Imagem 'chuvoso.png' não encontrada.")
                imagem = None

        # FUNÇÃO ATUALIZAR FUNDO
        janela.configure(bg=fundo)
        frame_corpo.configure(bg=fundo)
        ajustar_cores_texto(fundo)
        if imagem:
            imagem = imagem.resize((130, 130))
            imagem = ImageTk.PhotoImage(imagem)
            icon_lab.configure(image=imagem, bg=fundo)
            icon_lab.place(x=60, y=20)  # Posiciona a imagem na lateral direita
    else:
        cidade_lab['text'] = "Cidade não encontrada"
        data_lab['text'] = ""
        temperatura_lab['text'] = ""
        sensacao_lab['text'] = ""
        pressao_lab['text'] = ""
        humidade_lab['text'] = ""
        vento_lab['text'] = ""
        descricao_lab['text'] = ""

# FRAME TOP
pesquisa_local = tk.Entry(frame_top, width=20, justify="left", font=("", 15), highlightthickness=1, relief="solid")
pesquisa_local.place(x=15, y=10)
pesquisa_local.bind("<KeyRelease>", buscar_cidades)  # Chama a função ao digitar

# BOTÃO PESQUISA
botao_pesquisa = tk.Button(frame_top, command=informacao, width=10, text="Pesquisar", bg="lightblue", fg="black", font=("Ivy 10 bold"), relief="solid", overrelief=tk.RIDGE)
botao_pesquisa.place(x=250, y=10)

# FRAME CORPo
cidade_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 13 bold"))
cidade_lab.place(x=10, y=8)

data_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 13 bold"))
data_lab.place(x=10, y=60)

temperatura_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 35 bold"))
temperatura_lab.place(x=10, y=100)

sensacao_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 13"))
sensacao_lab.place(x=10, y=150)

pressao_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
pressao_lab.place(x=10, y=190)

humidade_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
humidade_lab.place(x=10, y=220)

vento_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
vento_lab.place(x=10, y=250)

descricao_lab = tk.Label(frame_corpo, text="", anchor="center", bg=fundo, fg=co1, font=("Arial 15 bold"))
descricao_lab.place(x=190, y=260)

# LOGO CENTRALIZADO
try:
    imagem_inicial = Image.open("image/logo.png") 
except FileNotFoundError:
    print("Erro: Arquivo 'logo.png' não encontrado na pasta 'image'. Continuando sem imagem inicial.")
    imagem_inicial = None

if imagem_inicial:
    imagem_inicial = imagem_inicial.resize((130, 130))
    imagem_inicial = ImageTk.PhotoImage(imagem_inicial)
    icon_lab = tk.Label(frame_corpo, image=imagem_inicial, bg=fundo)
    icon_lab.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 
else:
    icon_lab = tk.Label(frame_corpo, text="Logo", bg=fundo, fg=co1, font=("Arial", 12))
    icon_lab.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Vincular o evento de clique duplo à lista de cidades
lista_cidades.bind("<Double-Button-1>", selecionar_cidade)

# Iniciar a aplicação
janela.mainloop()