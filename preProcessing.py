import string
import nltk
from nltk.corpus import stopwords, wordnet

def preProcess(contenuto, isString=True):
    tokens = tokenize(contenuto)
    tokens = removePunctuation(tokens)
    if(isString):
        return ' '.join(tokens)
    else:
        return tokens

def tokenize(contenuto):
    return nltk.word_tokenize(contenuto)

def lemmatize(tokens):
    wnl = nltk.WordNetLemmatizer()
    return [wnl.lemmatize(x) for x in tokens]

def stem(tokens):
    porter = nltk.PorterStemmer()
    return [porter.stem(x) for x in tokens]

def removePunctuation(tokens):
    exclude = set(string.punctuation)
    return [x for x in tokens if x not in exclude]

def removeStopWords(tokens):
    return [x for x in tokens if x not in stopwords.words('english')]

def queryExpansion(query):
    query = query.lower()
    finalQuery = []
    count = 0
    for word in removeStopWords(removePunctuation(tokenize(query))):
        for synonyms in wordnet.synsets(word):
            for synonym in synonyms.lemmas():
                if count < 3:
                    syn = '(' + synonym.name().replace("_", " ").lower() + ')'
                    if syn not in finalQuery and syn not in '('+word+')':
                        finalQuery.append(syn)
                        count += 1
        count = 0
        query = ' '.join([q+'^2.0' for q in query.split()])
    return '(' + query + ') OR ' + ' OR '.join(['(' + fq[1:-1] + '^0.5)' for fq in finalQuery])