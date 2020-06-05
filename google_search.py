from googlesearch import search
import time

def google_search(query):
    my_results_list = []
    for i in search(query,  # The top level domain
                    lang = 'en',  # The language
                    num = 10,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = 29,    # Last result to retrieve
                    pause = 2.0,  # Lapse between HTTP requests
                   ):
        my_results_list.append(i)
    return my_results_list

queries = ["DNA"]
# queries = ["DNA"], "Apple", "Epigenetics", "Hollywood", "Maya", "Microsoft", "Precision", "Tuscany",
#            "99 balloons", "Computer Programming", "Financial meltdown", "Justin Timberlake",
#            "Least Squares", "Mars robots", "Page six", "Roman Empire", "Solar energy",
#            "Statistical Significance", "Steve Jobs", "The Maya", "Triple Cross", "US Constitution",
#            "Eye of Horus", "Madam I'm Adam", "Mean Average Precision", "Physics Nobel Prizes",
#            "Read the manual", "Spanish Civil War", "Do geese see god", "Much ado about nothing"]

l = []
for i in queries:
    l += google_search(i + " site:en.wikipedia.org")
    print(i)
    time.sleep(3)

print(l)