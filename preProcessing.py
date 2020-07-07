import string
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.corpus import wordnet as wn

def preProcess(contenuto, isString=True):
    tokens = tokenize(contenuto)
    tokens = removePunctuation(tokens)
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
        for token in query:
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
        return selScore
    else:
        return 0

def queryExpansion(query):
    finalQuery = []
    count = 0
    for word in removeStopWords(tokenize(query)):
        synonim_score = {}
        for synonims in wordnet.synsets(word):
            for syn in synonims.lemmas():
                synonim_score[syn.name().replace('_', ' ').lower()] = disambiguateTerms(tokenize(query), syn.name().replace('_', ' ').lower())
        synonim_score = {k: v for k, v in sorted(synonim_score.items(), key=lambda item: item[1])}
        count = 0
        for syn in synonim_score.keys():
            if count < 1:
                syn = '(' + syn + ')'
                if syn not in finalQuery and syn not in '(' + word + ')':
                    finalQuery.append(syn)
                    count += 1
    return query if len(finalQuery) == 0 else '(' + query + ') OR ' + ' OR '.join(finalQuery)