import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import math


def dist_euclidiana(p1, p2):
    soma = 0
    for i in range(len(p1)):
        soma = soma + (p2[i] - p1[i])**2
    distancia = math.sqrt(soma)
    return distancia


def le_arq():
    url = 'dados.csv'
    dados = pd.read_csv(url, header=None)
    dados = np.array(dados)
    return dados


dados = le_arq()
numObservacao = dados.shape[0]
index = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5]}
grupo = {0: [0], 1: [1], 2: [2], 3: [3], 4: [4], 5: [5]}
quantidadeGrupo = numObservacao - 1
tamanhoMatriz = len(index)
matriz_dendograma = np.zeros(((numObservacao-1), 4))
print(matriz_dendograma)
menor = 1000
mini = 1000
vetor_min = []
pos_min = [0, 0]
for z in range(tamanhoMatriz-1):
    matriz_similaridade = np.zeros((tamanhoMatriz, tamanhoMatriz))
    for i in range(len(list(index))):
        for j in range(len(list(index))):
            if j >= i:
                continue
            else:
                if len(index[list(index)[i]]) == 1 and len(index[list(index)[j]]) == 1:
                    matriz_similaridade[i][j] = round(
                        dist_euclidiana(dados[index[list(index)[i]][0]], dados[index[list(index)[j]][0]]), 3)
                elif len(index[list(index)[i]]) == 1 and len(index[list(index)[j]]) != 1:
                    menor = 1000
                    for q in range(len(index[list(index)[j]])):
                        dist = round(dist_euclidiana(
                            dados[index[list(index)[i]][0]], dados[index[list(index)[j]][q]]), 3)
                        if menor > dist:
                            menor = dist
                    matriz_similaridade[i][j] = menor
                elif len(index[list(index)[i]]) != 1 and len(index[list(index)[j]]) == 1:
                    menor = 1000
                    for q in range(len(index[list(index)[i]])):
                        dist = round(dist_euclidiana(
                            dados[index[list(index)[i]][q]], dados[index[list(index)[j]][0]]), 3)
                        if menor > dist:
                            menor = dist
                    matriz_similaridade[i][j] = menor
                else:
                    menor = 1000
                    for x in range(len(index[list(index)[i]])):
                        for y in range(len(index[list(index)[j]])):
                            dist = round(dist_euclidiana(
                                dados[index[list(index)[i]][x]], dados[index[list(index)[j]][y]]), 3)
                            if menor > dist:
                                menor = dist
                    matriz_similaridade[i][j] = menor
    print(matriz_similaridade)
    for i in range(tamanhoMatriz):
        for j in range(tamanhoMatriz):
            if j >= i:
                continue
            else:
                if matriz_similaridade[i][j] < mini:
                    mini = matriz_similaridade[i][j]
                    pos_min = [i, j]
    vetor_min.append(mini)
    print(pos_min)
    if len(index[list(index)[pos_min[0]]]) == 1:
        quantidadeGrupo = quantidadeGrupo + 1
        if len(index[list(index)[pos_min[1]]]) == 1:
            matriz_dendograma[z][0] = list(index)[pos_min[1]]
            matriz_dendograma[z][1] = list(index)[pos_min[0]]
            matriz_dendograma[z][2] = mini
            grupo.update({quantidadeGrupo: [list(index)[pos_min[1]], list(index)[pos_min[0]]]})
            grupo.pop(list(index)[pos_min[1]])
            grupo.pop(list(index)[pos_min[0]])
        else:
            for q in range(len(list(grupo))):
                if len(grupo[list(grupo)[q]]) == 1:
                    continue
                elif list(index)[pos_min[1]] not in grupo[list(grupo)[q]]:
                    continue
                else:
                    pos_aux = q
                    matriz_dendograma[z][0] = list(index)[pos_min[0]]
                    matriz_dendograma[z][1] = list(grupo)[q]
                    matriz_dendograma[z][2] = mini
                    grupo.update({quantidadeGrupo: grupo[list(grupo)[q]]})
                    grupo[quantidadeGrupo].append(list(index)[pos_min[0]])
            grupo.pop(list(grupo)[pos_aux])
            grupo.pop(list(index)[pos_min[0]])
        index[list(index)[pos_min[1]]].append(list(index)[pos_min[0]])
        matriz_dendograma[z][3] = len(index[list(index)[pos_min[1]]])
    else:
        quantidadeGrupo = quantidadeGrupo + 1
        if len(index[list(index)[pos_min[1]]]) == 1:
            for q in range(len(list(grupo))):
                if len(grupo[list(grupo)[q]]) == 1:
                    continue
                elif list(index)[pos_min[0]] not in grupo[list(grupo)[q]]:
                    continue
                else:
                    pos_aux = q
                    matriz_dendograma[z][0] = list(index)[pos_min[1]]
                    matriz_dendograma[z][1] = list(grupo)[q]
                    matriz_dendograma[z][2] = mini
                    grupo.update({quantidadeGrupo: grupo[list(grupo)[q]]})
                    grupo[quantidadeGrupo].append(list(grupo)[pos_min[1]])
            grupo.pop(list(grupo)[pos_aux])
            grupo.pop(list(grupo)[pos_min[1]])
        else:
            for q in range(len(list(grupo))):
                if len(grupo[list(grupo)[q]]) == 1:
                    continue
                elif (list(index)[pos_min[0]] or list(index)[pos_min[0]]) not in grupo[list(grupo)[q]]:
                    continue
                else:
                    pos_aux = q
                    matriz_dendograma[z][0] = list(grupo)[pos_min[0]]
                    matriz_dendograma[z][1] = list(grupo)[q]
                    matriz_dendograma[z][2] = mini
                    grupo.update({quantidadeGrupo: grupo[list(grupo)[q]]})
                    for s in range(len(grupo[list(grupo)[pos_min[1]]])):
                        grupo[quantidadeGrupo].append(
                            grupo[list(grupo)[pos_min[0]]][s])
            grupo.pop(list(grupo)[pos_aux])
            grupo.pop(list(grupo)[pos_min[1]])
        for s in range(len(index[list(index)[pos_min[0]]])):
            index[list(index)[pos_min[1]]].append(
                index[list(index)[pos_min[0]]][s])
        matriz_dendograma[z][3] = len(index[list(index)[pos_min[1]]])
    index.pop(list(index)[pos_min[0]])
    tamanhoMatriz = len(index)
    print(index)
    mini = 1000
    print(grupo)
print(matriz_dendograma)
dendrogram = dendrogram(matriz_dendograma, truncate_mode='none')
plt.title("Agrupamento Hierarquico")
plt.show()
