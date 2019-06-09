import pandas as pd
import numpy as np
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
tamanhoMatriz = len(index)
menor = 1000
mini = 1000
vetor_min = []
pos_min = [0, 0]
grupo = []
verificaIndexLinha = False
verificaIndexColuna = False
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
                if matriz_similaridade[i][j] <= mini:
                    mini = matriz_similaridade[i][j]
                    pos_min = [i, j]
    vetor_min.append(mini)
    mini = 1000
    if len(index[list(index)[pos_min[0]]]) == 1:
        index[list(index)[pos_min[1]]].append(list(index)[pos_min[0]])
    else:
        for s in range(len(index[list(index)[pos_min[0]]])):
            index[list(index)[pos_min[1]]].append(
                index[list(index)[pos_min[0]]][s])
    print(pos_min)
    index.pop(list(index)[pos_min[0]])
    tamanhoMatriz = len(index)
    print(index)
mini = 1000
print(vetor_min)
