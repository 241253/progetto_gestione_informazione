from whoosh.fields import *
from xmlparserSAX import pagina, getParsedPage
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

def removeStopwordsLemmatizeStemming(tokens):
    wnl = nltk.WordNetLemmatizer()
    porter = PorterStemmer()
    return [porter.stem(wnl.lemmatize(x)) for x in tokens if x not in stopwords.words('english')]

def contentTokenization(contenuto):
    tokens = nltk.word_tokenize(contenuto)
    tokens = removeStopwordsLemmatizeStemming(tokens)
    print(tokens) #indicizzare questa roba

#schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
#if not os.path.exists("indexdir"):
#    os.mkdir("indexdir")
#ix = create_in("indexdir", schema)
#
#writer = ix.writer()

#QUI
pagine = getParsedPage()
for p in pagine:
    contentTokenization(p.getContenuto())


#for p in pagine:
#    writer.add_document(title=p.getTitolo(), content=p.getContenuto(), path=u"https://en.wikipedia.org/wiki/"+p.getTitolo())
#writer.commit()

