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


# CREO IL NUOVO INDICE DI PROVA
schema = Schema(id=NUMERIC, title=TEXT(stored=True), body=TEXT(stored=True), paragraphTitle=TEXT(stored=True), category=TEXT(stored=True), infobox=TEXT(stored=True))
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
    writer.add_document(id=p.getId(), title=' '.join(contentTokenization(p.getTitolo())), body=' '.join(contentTokenization(p.getContenuto())), paragraphTitle=' '.join(contentTokenization(p.getTitoliParagrafi())), category=' '.join(contentTokenization(p.getCategoria())), infobox=' '.join(contentTokenization(p.getInfobox())))
writer.commit()
print('Fine creazione dell\'indice\n')