import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
import pandas as pd


def le_arq():
    url = 'iris.csv'
    dados = pd.read_csv(url, header=None)
    dados = np.array(dados)
    return dados


x = le_arq()
plt.scatter(x[:, 0], x[:, 1], s=10)
linkage_matrix = linkage(x, "complete", "euclidean")
print(linkage_matrix)
dendrogram = dendrogram(linkage_matrix, truncate_mode='none')
plt.title("Agrupamento Hierarquico")
plt.show()
