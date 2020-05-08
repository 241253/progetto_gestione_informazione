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


#CREO LO SCHEMA DELL'INDICE
schema_id = Schema(id=NUMERIC, title=TEXT(stored=True))

#CREO L'INDICE
if not os.path.exists("indexdir/index_id"):
   os.mkdir("indexdir/index_id")
id_ix = create_in("indexdir/index_id", schema_id)

#POPOLO L'INDICE
writer = id_ix.writer()
pagine = xmlparserSAX.getParsedPage()
print('Creazione del\'indice in corso...')
for p in pagine:
    writer. add_document(id=p.getId(), title=p.getTitolo())
    #contentTokenization(p.getContenuto())
writer.commit()
print('Fine creazione dell\'indice')