import webbrowser

import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

# APERTURA INDICE
ix_id = index.open_dir("indexdir/index_id")
ix_dict = index.open_dir("indexdir/index_dict")
search_type = 'termine'

# GUI
# Creazione finestra
window = Tk()
window.title("Il TOP SEARCHER di J e Z")
window.resizable(False, False)

# Creazione label verifica tipo di ricerca
lbl = Label(window, text='Ricerca per titolo:')
lbl.grid(columnspan=20, row=0)

# Creazione casella di testo
txt = Entry(window, width=125)
txt.grid(columnspan=18, row=1)

risultati = list()
for x in range(30):
    risultati.append((Label(window, text=""), Label(window, text="")))

def search_id(posting, index):
    for item in posting:
        q = QueryParser('id', schema=ix_id.schema)
        r = q.parse(item.split(':')[0])
        with ix_id.searcher() as s:
            results = s.search(r, limit=30)
            temp_text = ''
            for r in results:
                url = 'en.wikipedia.org/wiki/' + str(r['title'])
                risultati[index][0].configure(text=r['title'])
                risultati[index][1].configure(text=url, fg="blue", cursor="hand2")
                risultati[index][1].bind(f'<Button-{index+1}>', lambda event: webbrowser.open(url))
                index += 1
    return index


# Creazione bottone di ricerca
def search_clicked():
    q = QueryParser('termine', schema=ix_dict.schema)
    r = q.parse(txt.get())
    with ix_dict.searcher() as s:
        results = s.search(r, limit=30)
        temp_text = ''
        index = 0
        for r in results:
            index = search_id(r['posting'], index)
        while index < 30:
            risultati[index][0].configure(text="")
            risultati[index][1].configure(text="")
            index += 1

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

# Scrollview per visualizzare il risultato della ricerca
# scrollview = scrolledtext.ScrolledText(window, width=100, height=10)
# scrollview.grid(columnspan=2, row=4, sticky="nesw")

for x in range(30):
    Label(window, text=f'{x}.').grid(column=0, row=x+3)
    risultati[x][0].grid(columnspan=9, row=x+3)
    risultati[x][1].grid(column=10, columnspan=10, row=x+3)

# Loop finestra (mantiene la finestra aperta)
window.mainloop()
