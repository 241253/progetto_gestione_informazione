import xml.sax


class pagina:
    def __init__(self):
        self.titolo = ''
        self.infobox = ''
        self.contenuto = ''
        self.categoria = ''

    def setTitolo(self, titolo):
        self.titolo = titolo

    def setContenuto(self, contenuto):
        self.contenuto = self.contenuto + contenuto

    def getURL(self):
        return 'https://en.wikipedia.org/wiki/' + self.getTitolo()

    def getContenuto(self):
        return self.contenuto

    def getTitolo(self):
        return self.titolo
    
    def extractInformation(self):
        # text = self.getContenuto().split('\n')
        self._extractInfobox()
        # self._extractCategory(text)
        # self._extractContent(text)

    def _extractInfobox(self):
        print(self.contenuto.split('\n'))


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
    pagine.__getitem__(2).extractInformation()

