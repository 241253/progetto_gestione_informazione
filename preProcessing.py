import string
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.corpus import wordnet as wn

def preProcess(contenuto, isString=True):
    tokens = tokenize(contenuto)
    # tokens = removePunctuation(tokens)
    tokens = removeStopWords(tokens)
    # tokens = lemmatize(tokens)
    # tokens = stem(tokens)
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

def disambiguateTerms(query, termine):
    selSense = None
    selScore = 0.0
    for sinonimo in wn.synsets(termine, wn.NOUN):
        score_i = 0.0
        for token in query: # token term in t_i's context window
            if (termine==token):
                continue
            bestScore = 0.0
            for sinonimo_token in wn.synsets(token, wn.NOUN):
                tempScore = sinonimo.wup_similarity(sinonimo_token)
                if (tempScore>bestScore):
                    bestScore=tempScore
            score_i = score_i + bestScore
        if (score_i>selScore):
            selScore = score_i
            selSense = sinonimo_token
    if (selSense is not None):
        print(termine,": ",selSense,", ",selSense.definition())
        print("Score: ",selScore)
        return selScore
    else:
        print(termine,": --")
        return 0

def queryExpansion(query):
    finalQuery = []
    count = 0
    for word in tokenize(query):
        for synonyms in wordnet.synsets(word):
            for synonym in synonyms.lemmas():
                if count < 3:
                    syn = '(' + synonym.name().replace("_", " ").lower() + ')'
                    if syn not in finalQuery and syn not in '('+word+')':
                        finalQuery.append(syn)
                        count += 1
        count = 0
        query = ' '.join([q for q in query.split()])
    return query if len(finalQuery) == 0 else '(' + query + ') OR ' + ' OR '.join(['(' + fq[1:-1] + ')' for fq in finalQuery])