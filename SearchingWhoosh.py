import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

# APERTURA INDICE
ix = index.open_dir("indexdir/index_id")
search_type = 'termine'

# GUI
# Creazione finestra
window = Tk()
window.title("Il TOP SEARCHER di J e Z")
window.resizable(False, False)

# Creazione label verifica tipo di ricerca
lbl = Label(window, text='Ricerca per titolo:')
lbl.grid(columnspan=2, row=0)

# Creazione casella di testo
txt = Entry(window, width=125)
txt.grid(column=0, row=1)

# Creazione bottone di ricerca
def search_clicked():
    scrollview.delete('1.0', END)
    q = QueryParser(search_type, schema=ix.schema)  # QUERY SUL CONTENUTO
    r = q.parse(txt.get())
    with ix.searcher() as s:
        results = s.search(r, limit=30)
        temp_text = ''
        for r in results:
            scrollview.insert(END, r['title'] + '\n')
search_btn = Button(window, text="Cerca", command=search_clicked)
search_btn.grid(column=1, row=1)


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
content_btn.grid(column=0, row=3)

# Scrollview per visualizzare il risultato della ricerca
scrollview = scrolledtext.ScrolledText(window, width=100, height=10)
scrollview.grid(columnspan=2, row=4, sticky="nesw")

# Loop finestra (mantiene la finestra aperta)
window.mainloop()


