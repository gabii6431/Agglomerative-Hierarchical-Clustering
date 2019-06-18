from tkinter import *
from tkinter import filedialog
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
    url = filename
    dados = pd.read_csv(url, header=None)
    dados = np.array(dados)
    return dados


# SINGLE_LINK
def single_link():
    dados = le_arq()
    numObservacao = dados.shape[0]
    index = {}
    grupo = []
    for p in range(numObservacao):
        index.update({p: [p]})
        grupo.append(p)
    quantidadeGrupo = numObservacao - 1
    tamanhoMatriz = len(index)
    matriz_dendograma = np.zeros(((numObservacao-1), 4))
    print(matriz_dendograma)
    menor = 1000
    mini = 1000
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
        print(pos_min)
        if len(index[list(index)[pos_min[0]]]) == 1:
            quantidadeGrupo = quantidadeGrupo + 1
            matriz_dendograma[z][0] = grupo[list(index)[pos_min[0]]]
            matriz_dendograma[z][1] = grupo[list(index)[pos_min[1]]]
            if len(index[list(index)[pos_min[1]]]) == 1:
                grupo[list(index)[pos_min[0]]] = quantidadeGrupo
                grupo[list(index)[pos_min[1]]] = quantidadeGrupo
            else:
                grupo[list(index)[pos_min[0]]] = quantidadeGrupo
                for u in range(len(index[list(index)[pos_min[1]]])):
                    grupo[index[list(index)[pos_min[1]]][u]] = quantidadeGrupo
            index[list(index)[pos_min[1]]].append(list(index)[pos_min[0]])
            matriz_dendograma[z][2] = mini
            matriz_dendograma[z][3] = len(index[list(index)[pos_min[1]]])
        else:
            quantidadeGrupo = quantidadeGrupo + 1
            matriz_dendograma[z][0] = grupo[list(index)[pos_min[0]]]
            matriz_dendograma[z][1] = grupo[list(index)[pos_min[1]]]
            if len(index[list(index)[pos_min[1]]]) == 1:
                grupo[list(index)[pos_min[1]]] = quantidadeGrupo
                for u in range(len(index[list(index)[pos_min[0]]])):
                    grupo[index[list(index)[pos_min[0]]][u]] = quantidadeGrupo
            else:
                for u in range(len(index[list(index)[pos_min[0]]])):
                    grupo[index[list(index)[pos_min[0]]][u]] = quantidadeGrupo
                for v in range(len(index[list(index)[pos_min[1]]])):
                    grupo[index[list(index)[pos_min[1]]][v]] = quantidadeGrupo
            for s in range(len(index[list(index)[pos_min[0]]])):
                index[list(index)[pos_min[1]]].append(
                    index[list(index)[pos_min[0]]][s])
            matriz_dendograma[z][2] = mini
            matriz_dendograma[z][3] = len(index[list(index)[pos_min[1]]])
        index.pop(list(index)[pos_min[0]])
        tamanhoMatriz = len(index)
        print(index)
        mini = 1000
        print(grupo)
    print(matriz_dendograma)
    dendrogram(matriz_dendograma, truncate_mode='none')
    plt.title("Agrupamento Hierarquico")
    plt.show()


# COMPLETE_LINK
def complete_link():
    dados = le_arq()
    numObservacao = dados.shape[0]
    index = {}
    grupo = []
    for p in range(numObservacao):
        index.update({p: [p]})
        grupo.append(p)
    tamanhoMatriz = len(index)
    quantidadeGrupo = numObservacao - 1
    matriz_dendograma = np.zeros(((numObservacao-1), 4))
    maior = -1000
    mini = 1000
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
                        maior = -1000
                        for q in range(len(index[list(index)[j]])):
                            dist = round(dist_euclidiana(
                                dados[index[list(index)[i]][0]], dados[index[list(index)[j]][q]]), 3)
                            if maior < dist:
                                maior = dist
                        matriz_similaridade[i][j] = maior
                    elif len(index[list(index)[i]]) != 1 and len(index[list(index)[j]]) == 1:
                        maior = -1000
                        for q in range(len(index[list(index)[i]])):
                            dist = round(dist_euclidiana(
                                dados[index[list(index)[i]][q]], dados[index[list(index)[j]][0]]), 3)
                            if maior < dist:
                                maior = dist
                        matriz_similaridade[i][j] = maior
                    else:
                        maior = -1000
                        for x in range(len(index[list(index)[i]])):
                            for y in range(len(index[list(index)[j]])):
                                dist = round(dist_euclidiana(
                                    dados[index[list(index)[i]][x]], dados[index[list(index)[j]][y]]), 3)
                                if maior < dist:
                                    maior = dist
                        matriz_similaridade[i][j] = maior
        print(matriz_similaridade)
        for i in range(tamanhoMatriz):
            for j in range(tamanhoMatriz):
                if j >= i:
                    continue
                else:
                    if matriz_similaridade[i][j] <= mini:
                        mini = matriz_similaridade[i][j]
                        pos_min = [i, j]
        print(pos_min)
        if len(index[list(index)[pos_min[0]]]) == 1:
            quantidadeGrupo = quantidadeGrupo + 1
            matriz_dendograma[z][0] = grupo[list(index)[pos_min[0]]]
            matriz_dendograma[z][1] = grupo[list(index)[pos_min[1]]]
            if len(index[list(index)[pos_min[1]]]) == 1:
                grupo[list(index)[pos_min[0]]] = quantidadeGrupo
                grupo[list(index)[pos_min[1]]] = quantidadeGrupo
            else:
                grupo[list(index)[pos_min[0]]] = quantidadeGrupo
                for u in range(len(index[list(index)[pos_min[1]]])):
                    grupo[index[list(index)[pos_min[1]]][u]] = quantidadeGrupo
            index[list(index)[pos_min[1]]].append(list(index)[pos_min[0]])
            matriz_dendograma[z][2] = mini
            matriz_dendograma[z][3] = len(index[list(index)[pos_min[1]]])
        else:
            quantidadeGrupo = quantidadeGrupo + 1
            matriz_dendograma[z][0] = grupo[list(index)[pos_min[0]]]
            matriz_dendograma[z][1] = grupo[list(index)[pos_min[1]]]
            if len(index[list(index)[pos_min[1]]]) == 1:
                grupo[list(index)[pos_min[1]]] = quantidadeGrupo
                for u in range(len(index[list(index)[pos_min[0]]])):
                    grupo[index[list(index)[pos_min[0]]][u]] = quantidadeGrupo
            else:
                for u in range(len(index[list(index)[pos_min[0]]])):
                    grupo[index[list(index)[pos_min[0]]][u]] = quantidadeGrupo
                for v in range(len(index[list(index)[pos_min[1]]])):
                    grupo[index[list(index)[pos_min[1]]][v]] = quantidadeGrupo
            for s in range(len(index[list(index)[pos_min[0]]])):
                index[list(index)[pos_min[1]]].append(
                    index[list(index)[pos_min[0]]][s])
            matriz_dendograma[z][2] = mini
            matriz_dendograma[z][3] = len(index[list(index)[pos_min[1]]])
        index.pop(list(index)[pos_min[0]])
        tamanhoMatriz = len(index)
        print(index)
        mini = 1000
        print(grupo)
    print(matriz_dendograma)
    dendrogram(matriz_dendograma, truncate_mode='none')
    plt.title("Agrupamento Hierarquico")
    plt.show()



# INTERFACE


janela = Tk()
janela.title("Algoritmo não-supervisionado para agrupamento de dados")
janela["bg"] = "#04B4AE"
lb1 = Label(janela, text="Selecione a base de dados:         ", bg="white")
lb = Label(janela, text="Selecione o algoritmo:   ", bg="white")
lbinvisivel = Label(janela, text="                                      ", bg="white")


filename = ''


def selecionararquivo():
    global filename
    filename = filedialog.askopenfilename()


lbinvisivel1 = Label(janela,
                     text="                                   ",
                     bg="#04B4AE")
lbinvisivel1.grid(row=0, column=0)

lb1 = Label(janela,
            font="Arial 12",
            text="Selecione a base de dados:         ",
            bg="#04B4AE")
lb1.grid(row=1, column=0)

btn3 = Button(janela,
              font="Arial 10",
              text="SELECIONE O ARQUIVO",
              bg="#D8D8D8",
              command=selecionararquivo)
btn3.grid(row=1, column=1)

lbcaminho = Label(janela,
                  text=""+filename,
                  bg='#04B4AE')
lbcaminho.grid(row=2, column=1)

lbinvisivel = Label(janela,
                    text="                                      ",
                    bg="#04B4AE")
lbinvisivel.grid(row=2, column=0)


lb = Label(janela,
           font="Arial 12",
           text="Selecione o algoritmo:   ",
           bg="#04B4AE")
lb.grid(row=3, column=0)

btn1 = Button(janela,
              font="Arial 10",
              text="SINGLE-LINKAGE",
              width=20,
              bg="#D8D8D8",
              command=single_link)
btn1.grid(row=3, column=1)

btn2 = Button(janela,
              font="Arial 10",
              text="COMPLETE-LINKAGE",
              width=20,
              bg="#D8D8D8",
              command=complete_link)
btn2.grid(row=4, column=1)


# LxA+E+T
janela.geometry("450x150+500+200")
janela.mainloop()

