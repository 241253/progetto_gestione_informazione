import urllib

from googlesearch import search
from urllib.parse import unquote
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


def getTitle(s):
    l = s.replace('\n', '').split(':')
    temp = ''
    for x in range(2,len(l)):
        temp += l[x] + ('' if x == len(l) else ':')
    return temp[:-1]

def correctFormat(s):
    s=s.replace('_', ' ')
    s=s.replace('\n', '')
    return s

if __name__ == '__main__':
    file = open('ricerca.txt', 'r')
    pages = []
    with file:
        for x in file:
            pages.append(x)

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    driver = webdriver.Chrome()
    driver.get("https://en.wikipedia.org/wiki/Special:Export")
    url = driver.find_element_by_id('ooui-php-1')
    nome = driver.find_element_by_xpath('//textarea[@name="pages"]')
    button = driver.find_element_by_id('ooui-php-12')
    for p in pages:
        url.send_keys(Keys.CONTROL + "a")
        url.send_keys(Keys.BACKSPACE)
        url.send_keys(p)
        nome.send_keys(Keys.CONTROL + "a")
        nome.send_keys(Keys.BACKSPACE)
        nome.send_keys(correctFormat(unquote(p[30::])))
        button.click()
        time.sleep(0.35)
    driver.close()

    # id = []
    # with open('enwiki-20200520-pages-articles-multistream-index.txt', 'r', encoding='utf-8') as file:
    #     lines = file.readlines()
    #     for line in lines:
    #         if getTitle(line) in pages:
    #             print(getTitle(line),' --> ', line.split(':')[1])
    #             id.append(line.split(':')[1])
    # print('LUNGHEZZA: ', len(id))
