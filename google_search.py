from googlesearch import search
import time

def google_search(query):
    my_results_list = []
    for i in search(query,  # The top level domain
                    lang = 'en',  # The language
                    num = 10,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = 30,    # Last result to retrieve
                    pause = 2.0,  # Lapse between HTTP requests
                   ):
        my_results_list.append(i)
    return my_results_list


queries = ["DNA", "Apple", "Epigenetics", "Hollywood", "Maya", "Microsoft", "Precision", "Tuscany",
"99 balloons", "Computer Programming", "Financial meltdown", "Justin Timberlake",
"Least Squares", "Mars robots", "Page six", "Roman Empire", "Solar energy",
"Statistical Significance", "Steve Jobs", "The Maya", "Triple Cross", "US Constitution",
"Eye of Horus", "Madam I'm Adam", "Mean Average Precision", "Physics Nobel Prizes",
"Read the manual", "Spanish Civil War", "Do geese see god", "Much ado about nothing"]

def ricerca(i):
    l = google_search(queries[i] + " site:en.wikipedia.org")
    file = open('ricerca.txt', 'a')
    with file:
        for x in l:
            file.write(x+'\n')


if __name__ == '__main__':
    ricerca(12)