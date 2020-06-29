from math import log

import numpy as np
from sklearn.metrics import average_precision_score, ndcg_score

from whoosh import scoring, index
from whoosh.qparser import MultifieldParser
from whoosh.scoring import MultiWeighting, TF_IDF, Frequency

queries = ["DNA", "Apple", "Epigenetics", "Hollywood", "Maya", "Microsoft", "Precision", "Tuscany",
"99 balloons", "Computer Programming", "Financial meltdown", "Justin Timberlake",
"Least Squares", "Mars robots", "Page six", "Roman Empire", "Solar energy",
"Statistical Significance", "Steve Jobs", "The Maya", "Triple Cross", "US Constitution",
"Eye of Horus", "Madam I'm Adam", "Mean Average Precision", "Physics Nobel Prizes",
"Read the manual", "Spanish Civil War", "Do geese see god", "Much ado about nothing"]

def get_results(search_key, weighting):
    q = MultifieldParser(['title', 'body', 'category', 'infobox'], schema=ix.schema)
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

# def sklearn_ndcg_evaluation():
#     true_relevance = np.asarray([[6, 5, 4, 3, 2, 1, 1, 1, 1, 1]])
#     media = 0
#     for q in queries:
#         ground_truth = []
#         with open('evaluation_files/'+q, 'r') as file:
#             ground_truth = file.readlines()
#         risultati = get_results(q)
#         temp = []
#         point = 6
#         for r in risultati:
#             if r in ground_truth:
#                 temp.append(point if point > 0 else 1)
#             else:
#                 temp.append(0)
#             point -= 1
#         scores = np.asarray([temp])
#         res = ndcg_score(true_relevance, scores)
#         media += res
#         print(q, ": ", res, scores)
#     print('MEDIA: ', media/30)

def ndcg_evaluation(weighting):
    true_relevance = [6, 5, 4, 3, 2, 1, 1, 1, 1, 1]
    idcg = 6
    for i in range(2, len(true_relevance)):
        idcg += true_relevance[i] / log(i, 2)
    media = 0
    for q in queries:
        ground_truth = []
        with open('evaluation_files/'+q, 'r') as file:
            ground_truth = file.readlines()
        ground_truth = [x[:-1] for x in ground_truth]
        risultati = get_results(q, weighting)
        scores = []
        point = 6
        # print(risultati)
        # print(ground_truth)
        for r in risultati:
            if r in ground_truth:
                scores.append(point if point > 0 else 1)
            else:
                scores.append(0)
            point -= 1
        res = scores[0]
        for i in range(1, len(scores)):
            res += scores[i]/log(i+1, 2)
        res =res / idcg
        media += res
        # print(q, ": ", res, scores)
    print('MEDIA: ', media/30)

def map_evaluation(weighting):
    sumMeanAveragePrecision = 0.0
    for q in queries:
        ground_truth = []
        with open('evaluation_files/'+q, 'r') as file:
            ground_truth = file.readlines()
        ground_truth = [x[:-1] for x in ground_truth]
        risultati = get_results(q, weighting)
        precision = []
        countRilevanti = 0
        sumAveragePrecision = 0.0
        for i in range(len(risultati)):
            if risultati[i] in ground_truth:
                countRilevanti += 1
                sumAveragePrecision += countRilevanti / (i+1)
            precision.append(countRilevanti / (i+1))

        sumMeanAveragePrecision += sumAveragePrecision / len(ground_truth)
        # print(q, ":", sumAveragePrecision / len(ground_truth), precision)

    print('MEDIA: ', sumMeanAveragePrecision / 30 )

if __name__ == '__main__':
    ix = index.open_dir("indexdir/index")
    wBM25 = scoring.BM25F(B=0.75, title_B=2.0, body_B=1.0, category_B=1.0, infobox_B=1.0, K1=1.5)
    wtf = TF_IDF()

    # COMMENTO

    print("NDCG EVALUATION con BM25:")
    ndcg_evaluation(wBM25)
    print("NDCG EVALUATION con TF_IDF:")
    ndcg_evaluation(wtf)

    print("\n\n")

    print("MAP EVALUATION con BM25")
    map_evaluation(wBM25)
    print("MAP EVALUATION con TF_IDF")
    map_evaluation(wtf)