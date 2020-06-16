import urllib

from googlesearch import search
from urllib.parse import unquote
import time

def google_search(query):
    my_results_list = []
    for i in search(query,  # The top level domain
                    lang = 'en',  # The language
                    num = 40,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = 40,    # Last result to retrieve
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


# def getTitle(s):
#     l = s.replace('\n', '').split(':')
#     temp = ''
#     for x in range(2,len(l)):
#         temp += l[x] + ('' if x == len(l) else ':')
#     return temp[:-1]
#
# def correctFormat(s):
#     s=s.replace('_', ' ')
#     s=s.replace('\n', '')
#     return s
#
if __name__ == '__main__':
    ricerca(21)
#     file = open('ricerca.txt', 'r')
#     pages = []
#     with file:
#         for x in file:
#             pages.append(x)
#     pages = [correctFormat(unquote(i[30::])) for i in pages]
#
#     id = []
#     with open('enwiki-20200520-pages-articles-multistream-index.txt', 'r', encoding='utf-8') as file:
#         lines = file.readlines()
#         print(len(lines))
#         for line in lines:
#             if getTitle(line) in pages:
#                 print(getTitle(line),' --> ', line.split(':')[1])
#                 id.append(line.split(':')[1])
#     print('LUNGHEZZA: ', len(id))
#     print(id)
