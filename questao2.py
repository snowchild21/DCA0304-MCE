"""
Análise nodal pelo método de Jordan.

20/09/2025
"""

from matriz_vetor import MatrizQuadrada
from matriz_vetor import Vetor


def main():
    print("|================== Análise nodal pelo método de Jordan ==================|")
    print("| Matriz G (condutâncias), vetor v (tensões nodais) e vetor i (correntes) |")
    print("|=========================================================================|\n")

    """
    DEFINIÇÃO DO PROBLEMA
    """

    while True:
        """
        Valores predefinidos do código ou definidos pelo usuário (manual ou aleatoriamente).
        """
        fixo = input(
            ">> Você deseja usar valores predefinidos do código para a matriz G e o vetor i?\n --- Digite 1: para sim;\n --- Digite 2: para não.\n"
        )

        # Valores predefinidos do código
        if fixo == '1':
            matriz_fixa = [
                [1.5, -0.5, 0.0, 0.0],
                [-0.5, 1.5, -0.5, 0.0],
                [0.0, -0.5, 1.625, -0.5],
                [0.0, 0.0, -0.5, 0.6]
            ]
            vetor_fixo = [35.0, -10.0, 0.0, 2.0]

            qtd_nos = len(vetor_fixo)

            m_G = MatrizQuadrada(qtd_nos)
            v_i = Vetor(qtd_nos)

            m_G.preencher_fixo(matriz_fixa)
            v_i.preencher_fixo(vetor_fixo)
            break

        # Valores definidos pelo usuário
        elif fixo == '2':
            qtd_nos = int(input(">> Digite a quantidade de nós: "))
            m_G = MatrizQuadrada(qtd_nos)
            v_i = Vetor(qtd_nos)

            while True:
                manual_aleatorio = input(
                    ">> Você deseja preencher o sistema Gv = i...\n --- Digite 1: Manualmente;\n --- Digite 2: Aleatoriamente?\n")

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
                    continue
            break

        else:
            print("\n(!!!) ERRO: Por favor, digite apenas 1 ou 2.")
            continue

    """
    Exibição da matriz G e do vetor i.
    """
    print("\nMatriz G (condutâncias):")
    m_G.mostrar()
    print("\nVetor i (correntes):")
    v_i.mostrar()

    """
    RESOLUÇÃO DO SISTEMA LINEAR Gv = i PELO MÉTODO DE JORDAN
    """

    for i in range(qtd_nos):
        """
        Normalização da linha i
        """
        pivo = m_G[i][i]  # Pivô da linha i

        # Verifica se o pivô é zero
        if pivo == 0:
            # Tenta encontrar uma linha abaixo com um pivô não nulo
            trocou = False
            for k in range(i+1, qtd_nos):
                if m_G[k][i] != 0:
                    # Troca as linhas i e k
                    m_G[i], m_G[k] = m_G[k], m_G[i]
                    v_i[i], v_i[k] = v_i[k], v_i[i]
                    pivo = m_G[i][i]  # Atualiza o pivô após a troca
                    trocou = True
                    break

            if not trocou:
                print("\n|=======================================================================|")
                print(f"|  (!!!) ERRO: Não foi possível encontrar um pivô não nulo na coluna {i}. |")
                print("|=======================================================================|")
                return 0  # Para a execução se não for possível continuar

        # Normaliza a linha i pelo pivô
        for j in range(qtd_nos):
            m_G[i][j] = m_G[i][j] / pivo  # Matriz

        v_i[i] = v_i[i] / pivo  # Vetor

        """
        Zerar os elementos na coluna i, exceto o pivô
        """
        for k in range(qtd_nos):
            if k != i:
                fator = m_G[k][i]  # Elemento a ser zerado

                for j in range(qtd_nos):
                    m_G[k][j] = m_G[k][j] - fator * m_G[i][j]  # Matriz

                v_i[k] = v_i[k] - fator * v_i[i]  # Vetor

    """
    Exibição da matriz G e do vetor solução do sistema Gv = i.
    """
    print("\nMatriz G após aplicação do método de Jordan:")
    m_G.mostrar()
    print("\nVetor v (tensões nodais) solução do sistema Gv = i:")
    v_i.mostrar()


if __name__ == "__main__":
    main()
