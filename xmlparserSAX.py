import xml.sax
import bz2
from os import listdir
from os.path import isfile, join

class pagina:
    def __init__(self):
        self.id = ''
        self.titolo = ''
        self.infobox = ''
        self.contenuto = ''
        self.categoria = list()

    def setTitolo(self, titolo):
        self.titolo = self.titolo + titolo

    def setInfobox(self, infobox):
        self.infobox = infobox

    def setContenuto(self, contenuto):
        self.contenuto = self.contenuto + "\n" + contenuto

    def getURL(self):
        return 'https://en.wikipedia.org/wiki/' + self.getTitolo()

    def getContenuto(self):
        return self.contenuto

    def getTitolo(self):
        return self.titolo

    def getId(self):
        return self.id

    def setId(self, id):
        self.id += id

    def extractInformation(self):
        # estrae infobox
        self._extractInfobox(self.getContenuto().split('\n'))
        # estrae categorie
        self._extractCategory(self.getContenuto().split('\n'))
        # Potrebbe servire in futuro per elaboreare il contenuto che è rimasto
        # self._extractContent(self.getContenuto().split('\n'))

    def _extractInfobox(self, text):
        count = 1
        i = 0
        trovato = False
        tempInfoBox = ""
        indexStart = -1
        indexEnd = -1

        while i < len(text):
            if (text[i].__contains__("{{Infobox")):
                tempInfoBox += text[i][10:]
                indexStart = i
                trovato = True
            if (i != indexStart and trovato):
                if (text[i].__contains__("{{")):
                    count += 1
                if (text[i].__contains__("}}")):
                    count -= 1
                if (count == 0):
                    indexEnd = i
                    break
                tempInfoBox += "\n" + text[i]
            i += 1
        self.setInfobox(tempInfoBox)
        self.contenuto = '\n'.join(text[:indexStart]) + '\n' + '\n'.join(text[(indexEnd + 1):])

    def _extractCategory(self, text):
        trovato = False
        for line in reversed(text):
            if line[:11] == '[[Category:':
                self.categoria.append(line[11:-2])
                trovato = True
            elif (trovato):
                break

        tempText = ''
        for line in text:
            if line.__contains__('== References ==') or line.__contains__('== External links ==') or line[
                                                                                                     :11] == '[[Category:':
                break
            else:
                line = line.replace("'", "")
                line = line.replace('"', "")
                line = line.replace("`", "")
                tempText += line + '\n'
        self.contenuto = tempText

    def __str__(self):
        return f'ID:{self.id}\nTitolo:{self.titolo.encode("utf-8")}\nContenuto:{self.contenuto.encode("utf-8")}\n'


class countHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.primo_id = True
        self.pagine = []
        self.tempPagina = pagina()
        self.currentTag = ""

    def startElement(self, name, attr):
        self.currentTag = name
        if(name == 'page'):
            self.primo_id = True

    def characters(self, content):
        if content.strip() != '':
            if self.currentTag == 'title':
                self.tempPagina.setTitolo(content)
            elif self.currentTag == 'text':
                self.tempPagina.setContenuto(content)
            elif self.currentTag == 'id':
                if(self.primo_id == True):
                    self.tempPagina.setId(content)


    def endElement(self, name):
        if name == 'id':
            self.primo_id = False
        if name == 'page':
            self.tempPagina.extractInformation()
            self.pagine.append(self.tempPagina)
            self.tempPagina = pagina()

    def getPagine(self):
        return self.pagine


def getParsedPage():
    parser = xml.sax.make_parser()
    handler = countHandler()
    parser.setContentHandler(handler)

    pagine = list()
    dumps = [f for f in listdir("dump") if isfile(join("dump", f))]
    for d in dumps:
        # source_file = bz2.BZ2File('test_enwiki-20200520-pages-articles-multistream1.xml-p1p30303.bz2', "r")
        # for line in source_file:
        #     parser.feed(line.decode('utf-8'))
        # parser.parse('./wiki.xml')
        parser.parse("dump/" + d)
        pagine.extend(handler.getPagine())
    return pagine


if __name__ == '__main__':
    print('Inizio parsing')
    pagine = getParsedPage()
    print('Fine parsing')