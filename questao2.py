"""
Análise nodal pelo método de Jordan.

20/09/2025
"""

from matriz_vetor import MatrizQuadrada
from matriz_vetor import Vetor


def main():
    print("===== Análise nodal pelo método de Jordan =====")

    """
    Definição do problema.
    """

    qtd_nos = int(input(">> Digite a quantidade de nós: "))

    m_G = MatrizQuadrada(qtd_nos)
    v_i = Vetor(qtd_nos)

    while True:
        manual_aleatorio = input(
            ">> Você deseja preencher o sistema Gv = i...\n >>>> Digite 1: Manualmente;\n >>>> Digite 2: Aleatoriamente?\n"
        )

        if manual_aleatorio == '1':
            m_G.preencher_manual()
            v_i.preencher_manual()
            break

        elif manual_aleatorio == '2':
            m_G.preencher_aleatorio()
            v_i.preencher_aleatorio()
            break

        else:
            print("\n(!!!) ERRO: Por favor, digite apenas 1 ou 2.")

    print("\nMatriz G (condutâncias):")
    m_G.mostrar()
    print("\nVetor i (correntes):")
    v_i.mostrar()


if __name__ == "__main__":
    main()
