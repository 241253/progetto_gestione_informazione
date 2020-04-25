import whoosh.index as index
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os, os.path
import PySimpleGUI as sg #alternativa TKINTER

# ix = open_dir("indexdir")
# searcher = ix.searcher()
#
# lista = list()
# tipo_ricerca='title'
# listbox = sg.Listbox(values=lista, size=(5000, 5000))
#
# layout = [[sg.Text('Search engine JM', justification="center", size=(5000, 1))],
#           [sg.Button("Cerca"), sg.InputText(size=(5000, 1))],
#           [sg.Button('Ricerca nel titolo'), sg.Button('Ricerca nel contenuto')],
#           [listbox]]
#
# # Create the Window
# window = sg.Window('Search engine JM', layout)
#
# # Event Loop to process "events" and get the "values" of the inputs
# while True:
#     event, values = window.read()
#     if event in (None, 'Cancel'):   # if user closes window or clicks cancel
#         break
#     # if event in 'Cerca':
#     #     parser = QueryParser(tipo_ricerca, schema=ix.schema)
#     #     query = parser.parse(values[0])
#     #     results = searcher.search(query, terms=True)
#     #     lista = list()
#     #     if len(results) != 0:
#     #         for x in results:
#     #             lista.append(x['title'] + ': ' + x['path'] + f'   punteggio: {x.score}')
#     #     listbox.Update(values=lista)
#     # else:
#     #     if event=='Ricerca nel titolo':
#     #         tipo_ricerca='title'
#     #     else:
#     #         tipo_ricerca='content'
#
# window.close()

#APERTURA INDICE
ix = index.open_dir("indexdir")

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
        print(r)
    print('\n\nCONTENUTO')
    for r in resultsContent:
        print(r)