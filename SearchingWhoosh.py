import webbrowser
from whoosh import scoring
import whoosh.index as index
from whoosh.qparser import MultifieldParser
from tkinter import *
from whoosh.scoring import TF_IDF
from progetto_gestione_informazione.preProcessing import queryExpansion

displayed_results = list()

# Funzione che assegna l'url di una pagina ad un bottone
def callback(url):
    def wrap(u = url):
        webbrowser.open_new(u)
    return wrap

#algoritmo di ranking che usa whoosh
# wBM25 = scoring.BM25F(B=0.75, title_B=2.0, body_B=1.0, category_B=1.0, infobox_B=1.0, K1=1.5)
wBM25 = scoring.BM25F(B=0.75, title_B=2.0, body_B=1.0, K1=1.5)
mw = TF_IDF()

# Funzione di ricerca per termine (globale)
def search_clicked():
    global displayed_results
    # resetto interfaccia grafica (parte risultati)
    for item in displayed_results:
        item[0].destroy()
        item[1].destroy()
    displayed_results = list()

    q = MultifieldParser(['title', 'body'], schema=ix.schema)
    search_keyword = txt.get()
    search_keyword = queryExpansion(search_keyword)
    r = q.parse(search_keyword)
    with ix.searcher(weighting=mw) as searcher:
        results = searcher.search(r, limit=30)
        for r in results:
            url = str(r['url'])
            label_num = Label(window, text='0.')
            button_url = Button(window, text=r['title'], command=callback(url))
            displayed_results.append((label_num, button_url))

        for i in range(len(displayed_results)):
            displayed_results[i][0].configure(text=f'{i + 1}.')
            displayed_results[i][0].grid(column=0, row=i + 3)
            displayed_results[i][1].grid(column=1, row=i + 3, sticky='ew')

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

# Loop finestra (mantiene la finestra aperta)
window.mainloop()