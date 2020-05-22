import webbrowser
import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

# LOGICA
# Lista componenti grafici dei risultati
displayed_results = list()

# Funzione che assegna l'url di una pagina ad un bottone
def callback(url):
    def wrap(u = url):
        webbrowser.open_new(u)
    return wrap

# Funzione di ricerca per id
def search_id(posting, countUrl):
    l = list()
    for item in posting:
        q = QueryParser('id', schema=ix_id.schema)
        r = q.parse(item.split(':')[0])
        with ix_id.searcher() as searcher:
            results = searcher.search(r, limit=30)
            for r in results:
                url = 'en.wikipedia.org/wiki/' + str(r['title'])
                label_num = Label(window, text='0.')
                label_title = Label(window, text=r['title'])
                button_url = Button(window, text="Vai al sito", command=callback(url))
                l.append((label_num, label_title, button_url))
                countUrl += 1

            for i in range(len(l)):
                l[i][0].configure(text=f'{i + countUrl}.')
                l[i][0].grid(column=0, row=i + countUrl + 3)
                l[i][1].grid(columnspan=9, row=i + countUrl + 3)
                l[i][2].grid(column=10, columnspan=10, row=i + countUrl + 3)

    return countUrl, l

def search_clicked():
    global displayed_results
    # resetto interfaccia grafica (parte risultati)
    for item in displayed_results:
        print(item[0].cget('text'), item[1].cget('text'))
        item[0].destroy()
        item[1].destroy()
        item[2].destroy()
    displayed_results = list()

    q = QueryParser('termine', schema=ix_dict.schema)
    r = q.parse(txt.get())
    with ix_dict.searcher() as searcher:
        results = searcher.search(r, limit=30)
        countUrl = 0
        for r in results:
            countUrl, l = search_id(r['posting'], countUrl)
            for item in l:
                displayed_results.append(item)

# APERTURA INDICE
ix_id = index.open_dir("indexdir/index_id")
ix_dict = index.open_dir("indexdir/index_dict")
search_type = 'termine'

# GUI
# Creazione finestra
window = Tk()
window.title("Il TOP SEARCHER di J e Z")
window.resizable(True, True)

# Creazione label verifica tipo di ricerca
lbl = Label(window, text='Ricerca per titolo:')
lbl.grid(columnspan=20, row=0)

# Creazione casella di testo
txt = Entry(window, width=125)
txt.grid(columnspan=18, row=1)

# Creazione bottone di ricerca
search_btn = Button(window, text="Cerca", command=search_clicked)
search_btn.grid(column=18, columnspan=2, row=1)

# Creazione bottoni di selezione di tipo ricerca
def title_clicked():
    global search_type
    search_type = 'title'
    lbl.configure(text="Ricerca per titolo:")
title_btn = Button(window, text="Ricerca per titolo", command=title_clicked)
title_btn.grid(column=0, row=2)

def content_clicked():
    global search_type
    search_type = 'content'
    lbl.configure(text="Ricerca per contenuto:")
content_btn = Button(window, text="Ricerca per contenuto", command=content_clicked)
content_btn.grid(column=1, row=2)

# Loop finestra (mantiene la finestra aperta)
window.mainloop()