from math import log

from whoosh import scoring, index
from whoosh.qparser import MultifieldParser
from whoosh.scoring import TF_IDF

from preProcessing import preProcess, queryExpansion

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
    ground_truth = [x[:-1].lower() for x in ground_truth]
    return ground_truth

def get_results(search_key, weighting):
    # q = MultifieldParser(['title', 'body', 'category', 'infobox', 'paragraphTitle'], schema=ix.schema)
    q = MultifieldParser(['title', 'body'], schema=ix.schema)

    r = q.parse(preProcess(search_key))
    l = []
    with ix.searcher(weighting=weighting) as searcher:
        results = searcher.search(r, limit=20, )
        count = 0
        for r in results:
            # print(r['infobox'])
            if r['title'][:9] != 'Category:':
                l.append(r['title'])
                count += 1
            if count == 10:
                break
    return l


def ndcg_evaluation(weighting):
    true_relevance = [6, 5, 4, 3, 2, 1, 1, 1, 1, 1]
    idcg = 6
    for i in range(2, len(true_relevance)):
        idcg += true_relevance[i] / log(i, 2)
    media = 0
    for q in queries:
        ground_truth = get_ground_truth(q)
        risultati = get_results(q, weighting)
        scores = []
        point = 6
        if len(risultati) != 0:
            for r in risultati:
                if r in ground_truth:
                    scores.append(point if point > 0 else 1)
                else:
                    scores.append(0)
                point -= 1
            res = scores[0]
            for i in range(1, len(scores)):
                res += scores[i]/log(i+1, 2)
            res = res / idcg
        else:
            res = 0
        media += res
        # print(q, ": ", res, scores)
    print('MEDIA: ', media/30)

def map_evaluation(weighting):
    sumMeanAveragePrecision = 0.0
    for q in queries:
        ground_truth = get_ground_truth(q)
        risultati = get_results(q, weighting)
        precision = []
        countRilevanti = 0
        sumAveragePrecision = 0.0
        for i in range(len(risultati)):
            if risultati[i] in ground_truth:
                countRilevanti += 1
                sumAveragePrecision += countRilevanti / (i+1)
            precision.append(countRilevanti / (i+1))

        # sumMeanAveragePrecision += sumAveragePrecision / countRilevanti if countRilevanti != 0 else 0
        sumMeanAveragePrecision += sumAveragePrecision / len(ground_truth)
        # print(q, ":", sumAveragePrecision / len(ground_truth), precision)

    print('MEDIA: ', sumMeanAveragePrecision / 30)

if __name__ == '__main__':
    ix = index.open_dir("indexdir/index")
    # wBM25 = scoring.BM25F(B=0.75, title_B=2, paragraphTitle=1.5, body_B=1.25, category_B=0.5, infobox_B=0.75, K1=1.5)
    wBM25 = scoring.BM25F(B=0.75, K1=1.5)
    wtf = TF_IDF()

    print("NDCG EVALUATION con BM25:")
    ndcg_evaluation(wBM25)
    print("NDCG EVALUATION con TF_IDF:")
    ndcg_evaluation(wtf)

    print("\n")

    print("MAP EVALUATION con BM25")
    map_evaluation(wBM25)
    print("MAP EVALUATION con TF_IDF")
    map_evaluation(wtf)