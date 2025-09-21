"""
Análise nodal pelo método de Jordan.

21/09/2025
"""

import numpy as np


def metodo_jordan(G, i):
    """
    Resolve o sistema Gv = i pelo método de Jordan.

    Parâmetros:
        G: matriz quadrada de condutâncias (mho).
        i: vetor de correntes (A).

    Retorno:
        v: vetor solução com tensões nodais (A).
        G_id: matriz G transformada (deve ser identidade).
    """
    qtd_nos = len(i)
    G_id = G.copy()  # copia para transformação
    i = i.copy()

    for col in range(qtd_nos):
        pivo = G_id[col, col]

        # Troca linha se pivô for zero
        if pivo == 0:
            trocou = False
            for k in range(col + 1, qtd_nos):
                if G_id[k, col] != 0:
                    G_id[[col, k]] = G_id[[k, col]]
                    i[col], i[k] = i[k], i[col]
                    pivo = G_id[col, col]
                    trocou = True
                    break
            if not trocou:
                raise ValueError(
                    f"Pivô zero na coluna {col}, impossível continuar.")

        # Normaliza linha do pivô
        G_id[col, :] = G_id[col, :] / pivo
        i[col] = i[col] / pivo

        # Zera os elementos da coluna exceto o pivô
        for k in range(qtd_nos):
            if k != col:
                fator = G_id[k, col]
                G_id[k, :] = G_id[k, :] - fator * G_id[col, :]
                i[k] = i[k] - fator * i[col]

    return i, G_id


def mostrar_sistema(G, i):
    """
    Mostra o sistema G.v = i com 4 casas decimais.
    """
    n = len(i)
    print("\nSistema G.v = i:")
    for row in range(n):
        linha = "  ".join(f"{G[row, col]:>9.4f}" for col in range(n))
        print(f"| {linha} |  | v{row+1} | = | {i[row]:>9.4f} |")


def main():
    print("|================== Análise nodal pelo método de Jordan ==================|")
    print("| Matriz G (condutâncias), vetor v (tensões nodais) e vetor i (correntes) |")
    print("|=========================================================================|\n")

    # Definição do problema
    while True:
        fixo = input(
            ">> Deseja usar valores predefinidos do código para a matriz G e o vetor i?\n"
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
            break

        elif fixo == "2":
            qtd_nos = int(input(">> Digite a quantidade de nós: "))
            G = np.zeros((qtd_nos, qtd_nos), dtype=float)
            i = np.zeros(qtd_nos, dtype=float)

            while True:
                manual_aleatorio = input(
                    ">> Deseja preencher o sistema Gv = i manualmente ou aleatoriamente?\n"
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
                    G = np.round(
                        np.random.uniform(-5, 5, size=(qtd_nos, qtd_nos)), 4)
                    i = np.round(np.random.uniform(-10, 10, size=qtd_nos), 4)
                    break

                else:
                    print("\n(!!!) Digite apenas 1 ou 2.")
                    continue
            break
        else:
            print("\n(!!!) Digite apenas 1 ou 2.")
            continue

    # Mostra sistema inicial
    print("\nSistema inicial:")
    mostrar_sistema(G, i)
    input("\nPressione Enter para resolver o sistema pelo método de Jordan...")
    print("-"*75)

    # Resolução
    try:
        v, G_final = metodo_jordan(G, i)

        # Mostra sistema final (G identidade e vetor solução)
        print("\nSistema final (matriz identidade e vetor solução):")
        mostrar_sistema(G_final, v)
        print("-"*75)

        # Tensões nodais
        print("\nTensões nodais:")
        for idx, val in enumerate(v):
            print(f"v{idx+1} = {val:.4f} V")
        print("="*75)

    except ValueError as e:
        print(f"\nErro: {e}")


if __name__ == "__main__":
    main()
