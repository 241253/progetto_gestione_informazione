with open('./wiki.xml', 'r', encoding='utf-8') as file:
    data = file.readlines()
    count = 0
    with open('wiki.xml', 'a+', encoding='utf-8') as file2:
        for l in data:
            if '</page>' in l:
                count +=1
            file2.write(l)
            if count == 10:
                file2.write('</mediawiki>')
                break