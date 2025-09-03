"""
Gerador de sistemas lineares
"""

from matriz import MatrizQuadrada
from matriz import Vetor


def main():
    # Matriz A

    qtd_variaveis = int(input("Digite a quantidade de variáveis: "))

    m_A = MatrizQuadrada(qtd_variaveis)
    v_b = Vetor(qtd_variaveis)

    while True:
        manual_aleatorio = input(
            "Você deseja preencher o sistema Ax = b...\n - Digite 1: Manualmente;\n - Digite 2: Aleatoriamente?\n"
        )

        if manual_aleatorio == '1':
            m_A.preencher_manual()
            v_b.preencher_manual()
            break

        elif manual_aleatorio == '2':
            m_A.preencher_aleatorio()
            v_b.preencher_aleatorio()
            break

        else:
            print("\nERRO: Por favor, digite apenas 1 ou 2.")

    print("\nMatriz A:")
    m_A.mostrar()
    print("\nVetor b:")
    v_b.mostrar()


if __name__ == "__main__":
    main()
