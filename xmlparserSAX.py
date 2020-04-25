import xml.sax


class pagina:
    def __init__(self):
        self.titolo = ''
        self.infobox = ''
        self.contenuto = ''
        self.categoria = ''

    def setTitolo(self, titolo):
        self.titolo = titolo

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
    
    def extractInformation(self):
        self._extractInfobox(self.getContenuto().split('\n'))
        self._extractCategory(self.getContenuto().split('\n'))
        # self._extractContent(self.getContenuto().split('\n'))

    def _extractInfobox(self, text):
        count = 1
        i = 0
        trovato = False
        tempInfoBox = ""
        indexStart = -1
        indexEnd = -1

        while i < len(text):
            if(text[i].__contains__("{{Infobox")):
                tempInfoBox += text[i][10:]
                indexStart = i
                trovato = True
            if(i != indexStart and trovato):
                if(text[i].__contains__("{{")):
                    count += 1
                if(text[i].__contains__("}}")):
                    count -= 1
                if(count == 0):
                    indexEnd = i
                    break
                tempInfoBox += "\n" + text[i]
            i += 1
        self.setInfobox(tempInfoBox)
        self.contenuto = '\n'.join(text[:indexStart]) + '\n' + '\n'.join(text[(indexEnd+1):])

    def _extractCategory(self, text):
        for line in text:
            pass

    def _extractContent(self, text):
        for line in text:
            pass

    def __str__(self):
        return f'URL: {self.url.encode("utf-8")}\nTitolo:{self.titolo.encode("utf-8")}\nContenuto:{self.contenuto.encode("utf-8")}\n\n\n'


class countHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self.pagine = []
        self.tempPagina = pagina()
        self.currentTag = ""
        self.count = 0

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
            # self.tempPagina.extractInformation()
            self.pagine.append(self.tempPagina)
            self.tempPagina = pagina()

    def getPagine(self):
        return self.pagine


def getParsedPage():
    parser = xml.sax.make_parser()
    handler = countHandler()
    parser.setContentHandler(handler)
    parser.parse('./wiki.xml')
    return handler.getPagine()


if __name__ == '__main__':
    pagine = getParsedPage()
    pagine[2].extractInformation()
