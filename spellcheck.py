from spellchecker import SpellChecker

queries = ["DNA", "Apple", "Epigenetics", "Hollywood", "Maya", "Microsoft", "Precision", "Tuscany",
"99 balloons", "Computer Programming", "Financial meltdown", "Justin Timberlake",
"Least Squares", "Mars robots", "Page six", "Roman Empire", "Solar energy",
"Statistical Significance", "Steve Jobs", "The Maya", "Triple Cross", "US Constitution",
"Eye of Horus", "Madam I'm Adam", "Mean Average Precision", "Physics Nobel Prizes",
"Read the manual", "Spanish Civil War", "Do geese see god", "Much ado about nothing"]

queries = ' '.join([x.lower() for x in queries])

def isMispelled(query):
    query_tokens = query.split(' ')
    spell = SpellChecker()
    for token in query_tokens:
        if token != spell.correction(token):
            return True
    return False

def correct(query):
    query_tokens = query.split(' ')
    final_query = ''
    spell = SpellChecker()
    for word in query_tokens:
        correzione = ''
        if(isMispelled(word)):
            for candidate in spell.candidates(word):
                if candidate in queries:
                    correzione = candidate
            if correzione == '':
                correzione = spell.correction(word)
            final_query += ' ' + correzione
        else:
            final_query += ' ' + word
    return final_query[1:]

query = 'Apple Babana Chery'
query = query.lower()

if(isMispelled(query)):
    print(correct(query))
else:
    print("La parola era corretta.")