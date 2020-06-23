import numpy as np
from sklearn.metrics import average_precision_score, ndcg_score

# # EVALUATION
# # we have groud-truth relevance of some answers to a query:
#
# # we predict some scores (relevance) for the answers
# print(res)
from whoosh import scoring, index
from whoosh.qparser import MultifieldParser
from whoosh.scoring import MultiWeighting, TF_IDF, Frequency
from SearchingWhoosh import txt

queries = ["DNA", "Apple", "Epigenetics", "Hollywood", "Maya", "Microsoft", "Precision", "Tuscany",
"99 balloons", "Computer Programming", "Financial meltdown", "Justin Timberlake",
"Least Squares", "Mars robots", "Page six", "Roman Empire", "Solar energy",
"Statistical Significance", "Steve Jobs", "The Maya", "Triple Cross", "US Constitution",
"Eye of Horus", "Madam I'm Adam", "Mean Average Precision", "Physics Nobel Prizes",
"Read the manual", "Spanish Civil War", "Do geese see god", "Much ado about nothing"]

ix = index.open_dir("indexdir/index")
wBM25 = scoring.BM25F(B=0.75, title_B=2.0, body_B=1.0, category_B=1.0, infobox_B=1.0, K1=1.5)
mw = MultiWeighting(TF_IDF(), id=wBM25, keys=Frequency())


def get_results(search_key):
    q = MultifieldParser(['title', 'body', 'category', 'infobox'], schema=ix.schema)
    r = q.parse(search_key)
    l = []
    with ix.searcher(weighting=mw) as searcher:
        results = searcher.search(r, limit=20)
        count = 0
        for r in results:
            if r['title'][:9] != 'Category:':
                l.append(r['title'])
                count += 1
            if count == 10:
                break
    return l

true_relevance = np.asarray([[6, 5, 4, 3, 2, 1, 1, 1, 1, 1]])
for q in queries:
    ground_truth = []
    with open('evaluation_files/'+q, 'r') as file:
        ground_truth = file.readlines()
    risultati = get_results(q)
    temp = []
    point = 6
    for r in risultati:
        if r in ground_truth:
            temp.append(point if point > 0 else 1)
        else:
            temp.append(0)
        point -= 1
    scores = np.asarray([temp])
    res = ndcg_score(true_relevance, scores)
    print(q, ": ", res)
