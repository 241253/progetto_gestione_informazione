import webbrowser
from whoosh import scoring
import whoosh.index as index
from whoosh.qparser import MultifieldParser
from tkinter import *
from whoosh.scoring import TF_IDF
from progetto_gestione_informazione.preProcessing import queryExpansion
from progetto_gestione_informazione.spellcheck import isMispelled, correct


def correct_query():
    query = correct(txt.get())
    txt.delete(0, END)
    txt.insert(0, query)
    search_clicked()

displayed_results = list()
current_page = 0

def select_page():
    global current_page
    page_clear()
    if current_page == 0:
        page_display(0)
    elif current_page == 1:
        page_display(10)
    else:
        page_display(20)
    current_page = (current_page+1)%3

def page_display(start):
    position = 4
    for i in range(start, 10+start):
        if i < len(displayed_results):
            displayed_results[i][0].configure(text=f'{i + 1}.')
            displayed_results[i][0].grid(column=0, row=position)
            displayed_results[i][1].grid(columnspan=9, column=1, row=position, sticky='ew')
        else:
            break
        position += 1

def page_clear(clear=False):
    global displayed_results
    # resetto interfaccia grafica (parte risultati)
    for item in displayed_results:
        if clear:
            item[0].destroy()
            item[1].destroy()
        else:
            item[0].grid_remove()
            item[1].grid_remove()
    if clear:
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
    fc_btn.grid_remove()
    global current_page
    if len(displayed_results) != 0:
        page_clear(True)
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
    current_page = 0
    select_page()

    if isMispelled(txt.get()):
        fc_btn.grid(columnspan=10, row=2, sticky='ew')
        fc_btn.configure(text='Forse cercavi: ' + correct(txt.get()))

# APERTURA INDICE
ix = index.open_dir("indexdir/index")
search_type = 'id'

# GUI
# Creazione finestra
window = Tk()
window.title("Wikipedia Search Engine")
window.resizable(False, False)

# Creazione label verifica tipo di ricerca
lbl = Label(window, text='Inserisci qui sotto la tua ricerca:')
lbl.grid(columnspan=10, row=0)

# Creazione casella di testo
txt = Entry(window, width=50)
txt.grid(columnspan=8, row=1)

# Creazione bottone di ricerca
search_btn = Button(window, text="Cerca", command=search_clicked)
search_btn.grid(column=8, columnspan=2, row=1)

#bottone forse cercavi
fc_btn = Button(window, command=correct_query)
fc_btn.grid(columnspan=10, row=2, sticky='ew')
fc_btn.grid_remove()

#Selettore pagine
page1_btn = Button(window, text="pagina successiva", command=select_page)
page1_btn.grid(columnspan=10, row=3, sticky='ew')


# Loop finestra (mantiene la finestra aperta)
window.mainloop()