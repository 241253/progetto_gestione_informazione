import string

import nltk
from nltk.corpus import stopwords

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