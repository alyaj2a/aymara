#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import open
import Tkinter
from time import sleep
import tkFileDialog
from tkFileDialog import asksaveasfile
from Tkinter import *
from bktree import BKTree, levenshtein, dict_words

ruta = "" # La utilizaremos para almacenar la ruta del fichero

errors = []

l = 0
beg = 0
end = 0

def nuevo():
    global ruta
    mensaje.set("Nuevo fichero")
    ruta = ""
    texto.delete(1.0, "end")
    root.title("Mi editor")

def abrir():
    global ruta
    mensaje.set("Abrir fichero")
    ruta = tkFileDialog.askopenfilename(
        initialdir='.',
        filetypes=(("Ficheros de texto", "*.txt"),),
        title="Abrir un fichero de texto")

    if ruta != "":
        fichero = open(ruta, 'r')
        contenido = fichero.read()
        texto.delete(1.0,'end')
        texto.insert('insert', contenido)
        fichero.close()
        root.title(ruta + " - Mi editor")

def guardar():
    mensaje.set("Guardar fichero")
    if ruta != "":
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        guardar_como()

def guardar_como():
    global ruta
    mensaje.set("Guardar fichero como")

    fichero = tkFileDialog.asksaveasfile(title="Guardar fichero",
        mode="w", defaultextension=".txt")

    if fichero is not None:
        ruta = fichero.name
        contenido = texto.get(1.0,'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""


def is_right(word):
    resultado = BKT.query(word,1)
    if(len(resultado) == 0):
        return False,[]
    elif(resultado[0][0]==0):
        return True,[]
    else:
        return False,resultado

def word_proc(event=None):
    cursor_possition = texto.index(Tkinter.INSERT).split('.')
    l = int(cursor_possition[0])
    c = int(cursor_possition[1])-2
    get_word_on_index('%d.%d'%(l,c))

def get_word_on_index(cursor_possition='0.0'):
    global l,beg,end
    if cursor_possition == '0.0':
        print(cursor_possition)
        cursor_possition = texto.index(Tkinter.INSERT)
        print(cursor_possition)
    cursor_possition = cursor_possition.split('.')
    l = int(cursor_possition[0])
    c = int(cursor_possition[1])
    beg = c
    end = c

    while True:
        if (beg == 0 or texto.get('%d.%d'%(l,beg))==''):
            break
        elif (texto.get('%d.%d'%(l,beg))==' '):
            beg = beg + 1
            break
        elif (texto.get('%d.%d'%(l,beg))=='\n'):
            break
        beg = beg-1

    while True:
        if (end == 0 or texto.get('%d.%d'%(l,end))==''):
            break
        elif (texto.get('%d.%d'%(l,end))==' ') or (texto.get('%d.%d'%(l,end))=='\n'):
            break
        end = end+1

    text_on_cursor = texto.get('%d.%d'%(l,beg),'%d.%d'%(l,end))

    word_ok, results = is_right(text_on_cursor)

    if(not word_ok):
        texto.tag_add("here", '%d.%d'%(l,beg), '%d.%d'%(l,end))
        texto.tag_config("here", background="red", foreground="white")
        i = 0
        #borrando correcciones
        for a in alt_str:
            a.set("")
        #escribimos nuevas correcciones
        for r in results:
            alt_str[i].set(str(r[1]))
            i = i+1
            if(i==5):
                break
        print(results)
    return text_on_cursor

def focused(event=None):
    get_word_on_index()

def swap_alt0(event=None):
    texto.delete('%d.%d'%(l,beg),'%d.%d'%(l,end))
    texto.insert('%d.%d'%(l,beg),alt_str[0].get())
def swap_alt1(event=None):
    texto.delete('%d.%d'%(l,beg),'%d.%d'%(l,end))
    texto.insert('%d.%d'%(l,beg),alt_str[1].get())
def swap_alt2(event=None):
    texto.delete('%d.%d'%(l,beg),'%d.%d'%(l,end))
    texto.insert('%d.%d'%(l,beg),alt_str[2].get())
def swap_alt3(event=None):
    texto.delete('%d.%d'%(l,beg),'%d.%d'%(l,end))
    texto.insert('%d.%d'%(l,beg),alt_str[3].get())
def swap_alt4(event=None):
    texto.delete('%d.%d'%(l,beg),'%d.%d'%(l,end))
    texto.insert('%d.%d'%(l,beg),alt_str[4].get())

# Configuración de la raíz
root = Tk()
root.title("Mi editor")

# Menú superior
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nuevo", command=nuevo)
filemenu.add_command(label="Abrir", command=abrir)
filemenu.add_command(label="Guardar", command=guardar)
filemenu.add_command(label="Guardar como", command=guardar_como)
filemenu.add_separator()
filemenu.add_command(label="Salir", command=root.quit)
menubar.add_cascade(menu=filemenu, label="Archivo")

# Caja de texto central
texto = Text(root)
texto.pack(fill="both", expand=1)
texto.config(bd=0, padx=6, pady=4, font=("Consolas",12))

alt_str = [ StringVar(), StringVar(), StringVar(), StringVar(), StringVar() ]
for a_s in alt_str:
    a_s.set(" ")

alt_label = [
    Label(root, textvar=alt_str[0], justify='left'),
    Label(root, textvar=alt_str[1], justify='left'),
    Label(root, textvar=alt_str[2], justify='left'),
    Label(root, textvar=alt_str[3], justify='left'),
    Label(root, textvar=alt_str[4], justify='left')]

for a_l in alt_label:
    a_l.pack(side="left")


root.config(menu=menubar)
# Finalmente bucle de la apliación

root.bind("<space>", word_proc)
texto.bind("<Button-1>", focused)
texto.bind("<Left>", focused)
texto.bind("<Right>", focused)
texto.bind("<Up>", focused)
texto.bind("<Down>", focused)
alt_label[0].bind("<Button-1>",swap_alt0)
alt_label[1].bind("<Button-1>",swap_alt1)
alt_label[2].bind("<Button-1>",swap_alt2)
alt_label[3].bind("<Button-1>",swap_alt3)
alt_label[4].bind("<Button-1>",swap_alt4)

BKT = BKTree(levenshtein,
            dict_words('aymara'))

root.mainloop()
