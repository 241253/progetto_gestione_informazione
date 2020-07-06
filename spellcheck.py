from spellchecker import SpellChecker

def isMispelled(query):
    query_tokens = query.split(' ')
    spell = SpellChecker()
    for token in query_tokens:
        if token != spell.correction(token):
            return True
    return False

def correct(query):
    return ''

print(isMispelled('Aple Banana'))