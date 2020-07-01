import os

from whoosh.fields import *
from whoosh.index import create_in
import xmlparserSAX
from preProcessing import preProcess

# CREO IL NUOVO INDICE DI PROVA
# schema = Schema(id=NUMERIC, title=TEXT(stored=True), body=TEXT(stored=True), paragraphTitle=TEXT(stored=True), category=TEXT(stored=True), infobox=TEXT(stored=True))
schema = Schema(id=NUMERIC, title=TEXT(stored=True), body=TEXT(stored=True))

# CREO L'INDICE
if not os.path.exists("indexdir/index"):
    os.mkdir("indexdir/index")
index = create_in("indexdir/index", schema)

#POPOLO L'INDICE ID
writer = index.writer()
print('parsing dump wikipedia in corso...')
pagine = xmlparserSAX.getParsedPage()
print('parsing dump wikipedia terminato\n')

print('Creazione dell\'indice in corso...')
for p in pagine:
    # per usare il preprocessing scommentare la riga sottostante e commentare quella successiva
    # writer.add_document(id=p.getId(), title=preProcess(p.getTitolo()), body=preProcess(p.getContenuto()), paragraphTitle=preProcess(p.getTitoliParagrafi()), category=preProcess(p.getCategoria()), infobox=preProcess(p.getInfobox()))
    # writer.add_document(id=p.getId(), title=p.getTitolo(), body=p.getContenuto(), paragraphTitle=p.getTitoliParagrafi(), category=p.getCategoria(), infobox=p.getInfobox())
    writer.add_document(id=p.getId(), title=preProcess(p.getTitolo().lower()), body=preProcess(p.getContenuto().lower()))
writer.commit()
print('Fine creazione dell\'indice\n')