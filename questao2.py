"""
Análise nodal pelo método de Jordan (usando apenas NumPy).

21/09/2025
"""

import numpy as np


def metodo_jordan(G, i):
    """
    Resolve o sistema linear Gv = i pelo método de Jordan.
    
    Parâmetros:
        G (np.ndarray): matriz quadrada de condutâncias.
        i (np.ndarray): vetor de correntes.
    
    Retorno:
        v (np.ndarray): vetor solução com as tensões nodais.
    """
    qtd_nos = len(i)
    G = G.copy()
    i = i.copy()

    for col in range(qtd_nos):
        pivo = G[col, col]

        # Se pivô é zero → tenta trocar de linha
        if pivo == 0:
            trocou = False
            for k in range(col + 1, qtd_nos):
                if G[k, col] != 0:
                    G[[col, k]] = G[[k, col]]
                    i[col], i[k] = i[k], i[col]
                    pivo = G[col, col]
                    trocou = True
                    break
            if not trocou:
                raise ValueError(f"Não foi possível encontrar um pivô não nulo na coluna {col}.")

        # Normaliza a linha atual
        G[col, :] = G[col, :] / pivo
        i[col] = i[col] / pivo

        # Zera os elementos da coluna atual, exceto o pivô
        for k in range(qtd_nos):
            if k != col:
                fator = G[k, col]
                G[k, :] = G[k, :] - fator * G[col, :]
                i[k] = i[k] - fator * i[col]

    return i


def main():
    print("|================== Análise nodal pelo método de Jordan ==================|")
    print("| Matriz G (condutâncias), vetor v (tensões nodais) e vetor i (correntes) |")
    print("|=========================================================================|\n")

    """
    DEFINIÇÃO DO PROBLEMA
    """
    while True:
        fixo = input(
            ">> Você deseja usar valores predefinidos do código para a matriz G e o vetor i?\n"
            " --- Digite 1: para sim;\n"
            " --- Digite 2: para não.\n"
        )

        if fixo == "1":
            G = np.array([
                [1.5, -0.5, 0.0, 0.0],
                [-0.5, 1.5, -0.5, 0.0],
                [0.0, -0.5, 1.625, -0.5],
                [0.0, 0.0, -0.5, 0.6]
            ], dtype=float)

            i = np.array([35.0, -10.0, 0.0, 2.0], dtype=float)

            qtd_nos = len(i)
            break

        elif fixo == "2":
            qtd_nos = int(input(">> Digite a quantidade de nós: "))
            G = np.zeros((qtd_nos, qtd_nos), dtype=float)
            i = np.zeros(qtd_nos, dtype=float)

            while True:
                manual_aleatorio = input(
                    ">> Você deseja preencher o sistema Gv = i...\n"
                    " --- Digite 1: Manualmente;\n"
                    " --- Digite 2: Aleatoriamente?\n"
                )

                if manual_aleatorio == "1":
                    print("\nDigite os valores da matriz G:")
                    for a in range(qtd_nos):
                        for b in range(qtd_nos):
                            G[a, b] = float(input(f"G[{a}][{b}] = "))

                    print("\nDigite os valores do vetor i:")
                    for a in range(qtd_nos):
                        i[a] = float(input(f"i[{a}] = "))
                    break

                elif manual_aleatorio == "2":
                    G = np.round(np.random.uniform(-5, 5, size=(qtd_nos, qtd_nos)), 3)
                    i = np.round(np.random.uniform(-10, 10, size=qtd_nos), 3)
                    break

                else:
                    print("\n(!!!) ERRO: Por favor, digite apenas 1 ou 2.")
                    continue
            break

        else:
            print("\n(!!!) ERRO: Por favor, digite apenas 1 ou 2.")
            continue

    """
    Exibição da matriz G e do vetor i.
    """
    print("\nMatriz G (condutâncias):")
    print(G)
    print("\nVetor i (correntes):")
    print(i)

    """
    Resolução do sistema pelo método de Jordan
    """
    try:
        v = metodo_jordan(G, i)
        print("\nMatriz G após aplicação do método de Jordan:")
        print(np.round(G, 4))
        print("\nVetor v (tensões nodais) solução do sistema Gv = i:")
        print(np.round(v, 4))
    except ValueError as e:
        print(f"\nErro: {e}")


if __name__ == "__main__":
    main()
