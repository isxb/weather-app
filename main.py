import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

API_KEY= ""
cidade= 'pesquisa_local'

link = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}"

#################cores ###############
co0 = "#444466"  # Preta
co1 = "#feffff"  # branca
co2 = "#6f9fbd"  # azul

fundo_dia="#6cc4cc"
fundo_noite="#484f60"
fundo_tarde = "#bfb86d"

fundo = fundo_dia

janela = Tk()
janela.title("")
janela.geometry("350x400")
janela.configure(bg = fundo)

ttk.Separator(janela, orient=HORIZONTAL).grid(row=0, columnspan=1, ipadx=174)



#FRAMES

frame_top = Frame(janela, width=350, height=50, bg=co1, pady=0, padx=0)
frame_top.grid(row=1, column=0)

frame_corpo = Frame(janela, width=350, height=350, bg=fundo, pady=12, padx=0)
frame_corpo.grid(row=2, column=0, sticky=NW)


estilo = ttk.Style(janela)
estilo.theme_use("clam")


#CONFIG FRAME TOP

pesquisa_local = Entry(frame_top, width=20, justify="left", font=("", 15), highlightthickness=1, relief="solid")
pesquisa_local.place(x=15, y=10)


botao_pesquisa= Button(frame_top, width=10, text="Pesquisa", bg="lightblue", fg="black", font=("Ivy 10 bold"), relief="solid", overrelief=RIDGE)
botao_pesquisa.place(x=250, y=10)


#CONFIG FRAME CORPO

cidade_lab= Label(frame_corpo, text="Rio de Janeiro - Brasil / America do Sul",anchor="center", bg=fundo, fg=co1, font=("Arial", 13))
cidade_lab.place(x=10, y=8)


data_lab= Label(frame_corpo, text="21/03/2025 | 19:30:00 PM",anchor="center", bg=fundo, fg=co1, font=("Arial", 10))
data_lab.place(x=10, y=60)


humidade_lab= Label(frame_corpo, text="84",anchor="center", bg=fundo, fg=co1, font=("Arial", 40))
humidade_lab.place(x=10, y=100)


simbol_lab= Label(frame_corpo, text="%",anchor="center", bg=fundo, fg=co1, font=("Arial 10 bold"))
simbol_lab.place(x=85, y=110)


nome_lab= Label(frame_corpo, text="Humidade",anchor="center", bg=fundo, fg=co1, font=("Arial 8 bold"))
nome_lab.place(x=85, y=150)

pressao_lab= Label(frame_corpo, text="Pressão: 1000",anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
pressao_lab.place(x=10, y=190)

vento_lab= Label(frame_corpo, text="Velocidade do Vento: 1000",anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
vento_lab.place(x=10, y=220)

imagem = Image.open("image/chuvoso.png")
imagem = imagem.resize((130,130))
imagem = ImageTk.PhotoImage(imagem)

ceu_lab= Label(frame_corpo, text="Chovendo",anchor="center", bg=fundo, fg=co1, font=("Arial 10"))
ceu_lab.place(x=240, y=250)

icon_lab= Label(frame_corpo, image=imagem, bg=fundo)
icon_lab.place(x=200, y=120)




janela.mainloop()