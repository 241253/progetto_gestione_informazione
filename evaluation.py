# EVALUATION
# we have groud-truth relevance of some answers to a query:
import numpy as np
from sklearn.metrics import average_precision_score, ndcg_score

true_relevance = np.asarray([[6, 5, 4, 3, 2, 1, 1, 1, 1, 1]])
# we predict some scores (relevance) for the answers
scores = np.asarray([[0, 5, 0, 0, 0, 1, 1, 0, 1, 0]])
res = ndcg_score(true_relevance, scores)
print(res)

y_true = np.array([6, 5, 4, 3, 2, 1, 1, 1, 1, 1])
y_scores = np.array([0.0, 0.5, 0.0, 0.0, 0.0, 0.1, 0.1, 0.0, 0.1, 0.0])
average_precision_score(y_true, y_scores)