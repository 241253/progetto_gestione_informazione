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


#POPOLO L'INDICE LO SCHEMA
schema = Schema(title=TEXT(stored=True), content=TEXT)

#CREO L'INDICE
if not os.path.exists("indexdir"):
   os.mkdir("indexdir")
ix = create_in("indexdir", schema)


#POPOLO L'INDICE
#writer = ix.writer()
pagine = xmlparserSAX.getParsedPage()
for p in pagine:
    contentTokenization(p.getContenuto())
    #writer.add_document(title=p.getTitolo(), content=p.getContenuto())
#writer.commit()
print('Fine creazione dell\'indice')