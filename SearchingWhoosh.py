import webbrowser

from whoosh import scoring
import whoosh.index as index
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from tkinter import *

# LOGICA
# Lista componenti grafici dei risultati
from whoosh.scoring import MultiWeighting, TF_IDF, Frequency

displayed_results = list()

# Funzione che assegna l'url di una pagina ad un bottone
def callback(url):
    def wrap(u = url):
        webbrowser.open_new(u)
    return wrap

#algoritmo di ranking che usa whoosh
wBM25 = scoring.BM25F(B=0.75, title_B=2.0, body_B=1.0, category_B=1.0, infobox_B=1.0, K1=1.5)
mw = MultiWeighting(TF_IDF(), id=wBM25, keys=Frequency())

# Funzione di ricerca per termine (globale)
def search_clicked():
    global displayed_results
    # resetto interfaccia grafica (parte risultati)
    for item in displayed_results:
        item[0].destroy()
        item[1].destroy()
        item[2].destroy()
    displayed_results = list()

    q = MultifieldParser(['title', 'body', 'category', 'infobox', 'paragraphTitle'], schema=ix.schema)
    r = q.parse(txt.get())
    with ix.searcher(weighting=mw) as searcher:
        results = searcher.search(r, limit=30)
        # countUrl = 0
        for r in results:
            url = 'en.wikipedia.org/wiki/' + str(r['title'])
            label_num = Label(window, text='0.')
            label_title = Label(window, text=r['title'])
            button_url = Button(window, text="Vai al sito", command=callback(url))
            displayed_results.append((label_num, label_title, button_url))

        for i in range(len(displayed_results)):
            displayed_results[i][0].configure(text=f'{i + 1}.')
            displayed_results[i][0].grid(column=0, row=i + 3)
            displayed_results[i][1].grid(columnspan=9, row=i + 3)
            displayed_results[i][2].grid(column=10, columnspan=10, row=i + 3)

# APERTURA INDICE
ix = index.open_dir("indexdir/index")
search_type = 'id'

# GUI
# Creazione finestra
window = Tk()
window.title("Il TOP SEARCHER di J e Z")
window.resizable(False, True)

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