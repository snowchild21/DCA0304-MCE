"""
Matriz quadrada com preenchimento manual ou aleatório.
Vetor com preenchimento manual ou aleatório.

20/09/2025
"""

import random


class MatrizQuadrada:
    def __init__(self, tamanho):
        """
        Construtor da classe.
        Cria uma matriz quadrada com todos os valores inicializados em 0.
        """
        self.tamanho = tamanho
        self.matriz = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

    def preencher_manual(self):
        """
        Permite ao usuário preencher cada elemento da matriz.
        """
        print("\nDigite os valores da matriz:")
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                valor = float(input(f"Elemento [{i}][{j}]: "))
                self.matriz[i][j] = valor

    def preencher_aleatorio(self):
        """
        Gera valores aleatórios para cada elemento da matriz.
        """
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                self.matriz[i][j] = round(random.uniform(
                    0, 100), 5)  # valores entre 0 e 100

    def preencher_fixo(self, valor):
        """
        Preenche a matriz com um valor fixo.
        """
        self.matriz = valor

    def mostrar(self):
        """
        Mostra a matriz linha por linha.
        """
        print("Matriz:")
        for linha in self.matriz:
            print(linha)

    def __getitem__(self, index):
        return self.matriz[index]

    def __setitem__(self, index, value):
        self.matriz[index] = value


class Vetor:
    def __init__(self, tamanho):
        """
        Construtor da classe.
        Cria um vetor com todos os valores inicializados em 0.
        """
        self.tamanho = tamanho
        self.vetor = [0 for _ in range(tamanho)]

    def preencher_manual(self):
        """
        Permite ao usuário preencher cada elemento da matriz.
        """
        print("\nDigite os valores do vetor:")
        for i in range(self.tamanho):
            valor = float(input(f"Elemento[{i}]: "))
            self.vetor[i] = valor

    def preencher_aleatorio(self):
        """
        Gera valores aleatórios para cada elemento do vetor.
        """
        for i in range(self.tamanho):
            self.vetor[i] = round(random.uniform(
                0, 100), 5)  # valores entre 0 e 100

    def preencher_fixo(self, valor):
        """
        Preenche o vetor com um valor fixo.
        """
        self.vetor = valor

    def mostrar(self):
        """
        Mostra o vetor linha por linha.
        """
        print("Vetor:")
        for linha in self.vetor:
            print("[", linha, "]")

    def __getitem__(self, index):
        return self.vetor[index]

    def __setitem__(self, index, value):
        self.vetor[index] = value
