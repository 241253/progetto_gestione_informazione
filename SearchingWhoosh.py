import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext

#APERTURA INDICE
ix = index.open_dir("indexdir")

# GUI
# Creazione finestra
window = Tk()
window.title("Il TOP SEARCHER di J e Z")

# Creazione casella di testo
txt = Entry(window,width=100)
txt.grid(column=0, row=0)

# Creazione bottone di ricerca
btn = Button(window, text="Cerca")
btn.grid(column=1, row=0)

# Creazione bottoni di selezione di tipo ricerca
btn = Button(window, text="Per titolo")
btn.grid(column=0, row=1)
btn = Button(window, text="Per contenuto")
btn.grid(column=0, row=2)

# Scrollview per visualizzare il risultato della ricerca
scrollview = scrolledtext.ScrolledText(window,width=100,height=10)
scrollview.grid(columnspan=2, row=3, sticky="nesw")

# Loop finestra (mantiene la finestra aperta)
window.mainloop()

#CREO LA QUERY
qc = QueryParser('content', schema=ix.schema) #QUERY SUL CONTENUTO
qt = QueryParser('title', schema=ix.schema) #QUERY SUL TITOLO
rc = qc.parse(u'Miller')
rt = qt.parse(u'world')

with ix.searcher() as s:
    resultsContent = s.search(rc, limit=None)
    resultsTitle = s.search(rt, limit=None)
    print('TITOLO')
    for r in resultsTitle:
        print(r['title'])
    print('\n\nCONTENUTO')
    for r in resultsContent:
        print(r['title'])