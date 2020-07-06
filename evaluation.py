from math import log
from whoosh import scoring, index
from whoosh.qparser import MultifieldParser
from whoosh.scoring import TF_IDF
from graphics import MAP_graphic, NDCG_graphic
from preProcessing import queryExpansion, preProcess

queries = ["DNA", "Apple", "Epigenetics", "Hollywood", "Maya", "Microsoft", "Precision", "Tuscany",
"99 balloons", "Computer Programming", "Financial meltdown", "Justin Timberlake",
"Least Squares", "Mars robots", "Page six", "Roman Empire", "Solar energy",
"Statistical Significance", "Steve Jobs", "The Maya", "Triple Cross", "US Constitution",
"Eye of Horus", "Madam I'm Adam", "Mean Average Precision", "Physics Nobel Prizes",
"Read the manual", "Spanish Civil War", "Do geese see god", "Much ado about nothing"]

def get_ground_truth(query):
    ground_truth = []
    with open('evaluation_files/' + query, 'r') as file:
        ground_truth = file.readlines()
    ground_truth = [preProcess(x[:-1].lower()) for x in ground_truth]
    return ground_truth

def get_results(search_key, weighting):
    # q = MultifieldParser(['title', 'body', 'category', 'infobox', 'paragraphTitle'], schema=ix.schema)
    q = MultifieldParser(['title', 'body'], schema=ix.schema)

    search_key = search_key.lower()
    search_key = preProcess(search_key)
    # search_key = queryExpansion(search_key)
    # print(search_key)
    r = q.parse(search_key)
    l = []
    with ix.searcher(weighting=weighting) as searcher:
        results = searcher.search(r, limit=20)
        count = 0
        for r in results:
            if r['title'][:9] != 'Category:':
                l.append(r['title'])
                count += 1
            if count == 10:
                break
    return l


def ndcg_evaluation(weighting):
    x = []
    true_relevance = [6, 5, 4, 3, 2, 1, 1, 1, 1, 1]
    idcg = true_relevance[0]
    for i in range(1, len(true_relevance)):
        idcg += true_relevance[i] / log(i+1, 2)
    media = 0
    for q in queries:
        ground_truth = get_ground_truth(q)
        risultati = get_results(q, weighting)
        scores = []
        point = 6
        if len(risultati) != 0:
            for r in risultati:
                if r in ground_truth:
                    scores.append(true_relevance[ground_truth.index(r)])
                else:
                    scores.append(0)
                point -= 1
            res = scores[0]
            for i in range(1, len(scores)):
                res += scores[i]/log(i+1, 2)
            res = res / idcg
        else:
            res = 0.0
        media += res
        # print(q, ": ", res, scores)
        x.append(res)
    return (media/30), x

def map_evaluation(weighting):
    x = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    sumMeanAveragePrecision = 0.0
    for q in queries:
        relevant = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ground_truth = get_ground_truth(q)
        risultati = get_results(q, weighting)
        precision = []
        countRilevanti = 0

        for i in range(len(risultati)):
            if risultati[i] in ground_truth:
                relevant[i] = 1
                countRilevanti += 1
                precision.append(countRilevanti / (i+1))
        for _ in range(10-len(precision)):
            precision.append(0)

        precision.reverse()
        for i in range(1, len(precision)):
            if precision[i] < precision[i-1]:
                precision[i] = precision[i-1]
        precision.append(precision[9])
        precision.reverse()

        for i in range(len(precision)):
            x[i] += precision[i]

        sumMeanAveragePrecision += sum(precision) / 11
        # print(q, ":", precision, relevant)
    # print([i/30 for i in x])
    return (sumMeanAveragePrecision / 30), [i/30 for i in x]

if __name__ == '__main__':
    ix = index.open_dir("indexdir/index")
    wBM25 = scoring.BM25F(B=0.75, title_B=1.0, body_B=0.5, K1=2)
    wtf = TF_IDF()

    m, y = ndcg_evaluation(wBM25)
    print("NDCG EVALUATION con BM25:", m)
    NDCG_graphic(y)
    m, y = ndcg_evaluation(wtf)
    print("NDCG EVALUATION con TF_IDF:", m)
    NDCG_graphic(y, 'TF_IDF')
    print()
    x = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    m, y = map_evaluation(wBM25)
    print("MAP EVALUATION con BM25", m)
    MAP_graphic(x, y)
    m, y = map_evaluation(wtf)
    print("MAP EVALUATION con TF_IDF", m)
    MAP_graphic(x, y, 'TF_IDF')