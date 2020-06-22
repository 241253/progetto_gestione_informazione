import os
import string

from whoosh.fields import *
from whoosh.index import create_in
import xmlparserSAX
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def tokensCleaner(tokens):
    #processo di lemmatizzazione e stemmatizzazione
    wnl = nltk.WordNetLemmatizer()
    porter = PorterStemmer()
    exclude = set(string.punctuation)
    #rimozione stopwords e punteggiature
    stopwordsToken = [porter.stem(wnl.lemmatize(x)) for x in tokens if x not in stopwords.words('english')]
    return [x for x in stopwordsToken if x not in exclude]


def contentTokenization(contenuto):
    tokens = nltk.word_tokenize(contenuto)
    tokens = tokensCleaner(tokens)
    return tokens


#CREO LO SCHEMA DELL'INDICE DEGLI ID
schema_id = Schema(id=NUMERIC, title=TEXT(stored=True))
#CREO LO SCHEMA DELL'INDICE DEL DIZIONARIO
schema_dict = Schema(termine=TEXT(stored=True), posting=TEXT(vector=True, stored=True))

#CREO L'INDICE DELL'ID
if not os.path.exists("indexdir/index_id"):
   os.mkdir("indexdir/index_id")
id_ix = create_in("indexdir/index_id", schema_id)
#CREO L'INDICE DEL DIZIONARIO
if not os.path.exists("indexdir/index_dict"):
   os.mkdir("indexdir/index_dict")
dict_ix = create_in("indexdir/index_dict", schema_dict)

#DIZIONARIO (CHE DIVENTA L'INDICE)
dizionario = dict()

def add_term(token, id):
    if token not in dizionario.keys():
        dizionario[token] = dict()
        dizionario[token][id] = 1
    else:
        d = dizionario[token]
        if id not in d.keys():
            d[id] = 1
        else:
            d[id] += 1


#POPOLO L'INDICE ID
start_time = datetime.time
writer_id = id_ix.writer()
print('parsing dump wikipedia in corso...')
pagine = xmlparserSAX.getParsedPage()
print('parsing dump wikipedia finito...\n')
print('Creazione dell\'indice id in corso...')
for p in pagine:
    writer_id.add_document(id=p.getId(), title=p.getTitolo())
    tokens = contentTokenization(p.getContenuto())
    for t in tokens:
        add_term(t, p.getId())
writer_id.commit()
print('Fine creazione dell\'indice id\n')

print('Creazione dell\'indice dict in corso...')
#POPOLO L'INDICE DICT
writer_dict = dict_ix.writer()
for d in dizionario.keys():
    l = list()
    for x in dizionario[d].keys():
        l.append(f'{x}:{dizionario[d][x]}')
    writer_dict.add_document(termine=d, posting=l)
writer_dict.commit()
print('Fine creazione dell\'indice dict\n')
print('sono passati: ', datetime.time - start_time, ' secondi')