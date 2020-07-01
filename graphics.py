import matplotlib.pyplot as plt
import numpy as np


def MAP_graphic(x, y, weighting_alg='BM25'):
    plt.plot(x, y, 'b-')
    plt.title('MAP with ' + weighting_alg)
    plt.xlabel('Recal')
    plt.ylabel('Precision')
    plt.show()

def NDCG_graphic(y, weighting_alg='BM25'):
    bars = 30
    x_pos = np.arange(30)
    plt.bar(x_pos, y)
    plt.xlabel('Queries')
    plt.title('NDCG with ' + weighting_alg)
    plt.tight_layout()
    plt.show()