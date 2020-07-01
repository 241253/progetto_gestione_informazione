import matplotlib.pyplot as plt

def MAP_graphic(x, y, weighting_alg='BM25'):
    plt.plot(x, y, 'b-')
    plt.title('MAP with ' + weighting_alg)
    plt.xlabel('Recal')
    plt.ylabel('Precision')
    plt.show()

def NDCG_graphic(x, weighting_alg='BM25'):
    fig, ax = plt.subplots()  # creiamo Figure and Axes in un comando solo

    # aggiungiamo l'istogramma
    # in questo caso hist ritorna tre valori che mettiamo in altrettante variabili
    n, bins, columns = ax.hist(x, 30, rwidth=0.5)

    ax.set_xlabel('ma io ')
    ax.set_ylabel('che cazzo ne so')
    ax.set_title('NDCG with ' + weighting_alg)
    fig.tight_layout()
    plt.show()