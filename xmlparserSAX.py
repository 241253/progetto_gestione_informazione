import xml.sax
from os import listdir
from os.path import isfile, join

paragraphTitle_exclude = ['references', 'external links', 'see also', 'notes', 'sources', 'bibliography']

class pagina:
    def __init__(self):
        self.id = ''
        self.titolo = ''
        self.infobox = ''
        self.contenuto = ''
        self.categoria = list()
        self.titoliParagrafi = list()

    def setTitolo(self, titolo):
        self.titolo = self.titolo + titolo

    def setInfobox(self, infobox):
        self.infobox = infobox

    def setContenuto(self, contenuto):
        self.contenuto = self.contenuto + "\n" + contenuto

    def setId(self, id):
        self.id += id

    def getURL(self):
        return 'https://en.wikipedia.org/wiki/' + self.getTitolo()

    def getContenuto(self):
        return self.contenuto

    def getTitolo(self):
        return self.titolo

    def getId(self):
        return self.id

    def getCategoria(self):
        return '\n'.join(self.categoria)

    def getInfobox(self):
        return self.infobox

    def getTitoliParagrafi(self):
        return '\n'.join(self.titoliParagrafi)

    def extractInformation(self, infobox=False, category=False, paragraphTitle=False):
        # Estrae infobox
        if infobox:
            self._extractInfobox(self.getContenuto().split('\n'))
        # Estrae categorie
        if category:
            self._extractCategory(self.getContenuto().split('\n'))
        # Estrae titoli dei paragrafi
        if paragraphTitle:
            self._extractParagraphTitle(self.getContenuto().split('\n'))

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
                # if text[i] != 'br':
                tempInfoBox += "\n" + text[i]
            i += 1
        # tempInfoBox = tempInfoBox.replace('[', '')
        # tempInfoBox = tempInfoBox.replace('{', '')
        # tempInfoBox = tempInfoBox.replace(']', '')
        # tempInfoBox = tempInfoBox.replace('}', '')
        # tempInfoBox = tempInfoBox.replace('>', '')
        # tempInfoBox = tempInfoBox.replace('<', '')
        # tempInfoBox = tempInfoBox.replace('|', '')

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
            if line.__contains__('== References ==') or line.__contains__('== External links ==') or line[:11] == '[[Category:':
                break
            else:
                line = line.replace("'", "")
                line = line.replace('"', "")
                line = line.replace("`", "")
                tempText += line + '\n'
        self.contenuto = tempText

    def _extractParagraphTitle(self, text):
        for line in text:
            if line[0:2] == '==' and line[-2:] == '==':
                self.titoliParagrafi.append(line.replace('=', ''))
        self.titoliParagrafi = [line.strip() for line in self.titoliParagrafi if line.lower().strip() not in paragraphTitle_exclude ]



    def __str__(self):
        return f'ID:{self.id}\nTitolo:{self.titolo.encode("utf-8")}\nContenuto:{self.contenuto.encode("utf-8")}\n'


class countHandler(xml.sax.handler.ContentHandler):
    def __init__(self, infobox=False, category=False, paragraphTitle=False):
        self.primo_id = True
        self.pagine = []
        self.tempPagina = pagina()
        self.currentTag = ""
        self.extract_infobox = infobox
        self.extract_category = category
        self.extract_paragraphTitle = paragraphTitle


    def startElement(self, name, attr):
        self.currentTag = name
        if (name == 'page'):
            self.primo_id = True

    def characters(self, content):
        if content.strip() != '':
            if self.currentTag == 'title':
                self.tempPagina.setTitolo(content)
            elif self.currentTag == 'text':
                self.tempPagina.setContenuto(content)
            elif self.currentTag == 'id':
                if (self.primo_id == True):
                    self.tempPagina.setId(content)

    def endElement(self, name):
        if name == 'id':
            self.primo_id = False
        if name == 'page':
            self.tempPagina.extractInformation(infobox=self.extract_infobox, category=self.extract_category, paragraphTitle=self.extract_paragraphTitle)
            self.pagine.append(self.tempPagina)
            self.tempPagina = pagina()

    def getPagine(self):
        return self.pagine


def pagina_non_presente(pagine, titolo_pagina):
    for p in pagine:
        if(p.getTitolo() == titolo_pagina):
            return False
    return True

def getParsedPage(infobox=False, category=False, paragraphTitle=False):
    parser = xml.sax.make_parser()
    pagine = list()
    dumps = [f for f in listdir("dump") if isfile(join("dump", f))]
    for d in dumps:
        handler = countHandler(infobox=infobox, category=category, paragraphTitle=paragraphTitle)
        parser.setContentHandler(handler)
        parser.parse("dump/" + d)
        if(len(handler.getPagine()) != 0 and pagina_non_presente(pagine, handler.getPagine()[0].getTitolo())):
            pagine.extend(handler.getPagine())
    return pagine


if __name__ == '__main__':
    print('Inizio parsing')
    pagine = getParsedPage(paragraphTitle=True)
    print('Fine parsing')
    print(len(pagine))
    print()
    for _ in range(20):
        print(pagine[_].getTitoliParagrafi())
        print()