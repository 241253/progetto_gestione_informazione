import xml.sax
import bz2


class pagina:
    def __init__(self, id):
        self.id = id
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
        return f'Titolo:{self.titolo.encode("utf-8")}\nContenuto:{self.contenuto.encode("utf-8")}\n\n\n'


class countHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.pagine = []
        self.tempPagina = pagina(0)
        self.currentTag = ""
        self.id = 1

    def startElement(self, name, attr):
        self.currentTag = name

    def characters(self, content):
        if content.strip() != '':
            if self.currentTag == 'title':
                self.tempPagina.setTitolo(content)
            elif self.currentTag == 'text':
                self.tempPagina.setContenuto(content)

    def endElement(self, name):
        if name == 'page':
            self.tempPagina.extractInformation()
            self.pagine.append(self.tempPagina)
            self.tempPagina = pagina(self.id)
            self.id += 1

    def getPagine(self):
        return self.pagine


def getParsedPage():
    parser = xml.sax.make_parser()
    handler = countHandler()
    parser.setContentHandler(handler)
    source_file = bz2.BZ2File('test_enwiki-20200520-pages-articles-multistream1.xml-p1p30303.bz2', "r")
    for line in source_file:
        parser.feed(line.decode('utf-8'))
    # parser.parse('./wiki.xml')
    return handler.getPagine()


if __name__ == '__main__':
    print('inizio parsing')
    pagine = getParsedPage()
    print('fine parsing')

    for x in range(10):
        print(pagine[x])
