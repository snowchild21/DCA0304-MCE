"""
Análise nodal pelo método da Fatoração LU.

21/09/2025
"""

import numpy as np
import matplotlib.pyplot as plt


def fatoracao_LU(A):
    """
    Este método consiste em quebrar o sistema Gv = i em dois sistemas triangulares:
        G = LU  (fatoração LU)
        (LU)v = i
        Ly = i   (substituição direta, pois L é triangular inferior)
        Uv = y   (substituição reversa, pois U é triangular superior)

    Ao resolvermos esses dois sistemas, obtemos o vetor v.
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]

    if A.shape[0] != A.shape[1]:
        raise ValueError("Erro crítico: a matriz deve ser quadrada.")

    L = np.zeros((n, n), dtype=float)
    U = np.zeros((n, n), dtype=float)

    for i in range(n):
        L[i, i] = 1.0

    for k in range(n):
        soma_u = sum(L[k, m] * U[m, k] for m in range(k))
        U[k, k] = A[k, k] - soma_u

        if abs(U[k, k]) < 1e-15:
            raise ZeroDivisionError(
                f"Erro crítico: pivô U[{k},{k}] é zero. Fatoração LU falhou."
            )

        for j in range(k + 1, n):
            soma_u = sum(L[k, m] * U[m, j] for m in range(k))
            U[k, j] = A[k, j] - soma_u

        for i in range(k + 1, n):
            soma_l = sum(L[i, m] * U[m, k] for m in range(k))
            L[i, k] = (A[i, k] - soma_l) / U[k, k]

    return L, U


def substituicao_direta(L, b):
    """Resolve o sistema Ly = b."""
    n = L.shape[0]
    y = np.zeros(n, dtype=float)

    for i in range(n):
        soma = sum(L[i, j] * y[j] for j in range(i))
        y[i] = b[i] - soma

    return y


def substituicao_reversa(U, y):
    """Resolve o sistema Uv = y."""
    n = U.shape[0]
    v = np.zeros(n, dtype=float)

    for i in range(n - 1, -1, -1):
        soma = sum(U[i, j] * v[j] for j in range(i + 1, n))
        v[i] = (y[i] - soma) / U[i, i]

    return v


def main():
    print("|==================== Análise nodal por Fatoração LU =====================|")
    print("| Matriz G (condutâncias), vetor v (tensões nodais) e vetor i (correntes) |")
    print("|=========================================================================|\n")

    # Definição da matriz G do circuito
    G = np.array([
        [-4.0,  1.0,   2.0,   0.0],
        [ 1.0, -4.0,   0.0,   2.0],
        [ 2.0,  0.0, -24.0,  20.0],
        [ 0.0,  2.0,  20.0, -24.0]
    ])

    print("\nMatriz de Condutâncias (G) do circuito [mho]:\n")
    print(G)
    print("-" * 73)
    input("\nPressione Enter para avançar")

    # Definição da fonte de corrente
    while True:
        try:
            entrada = input("\n>> Digite o valor da corrente I (em Amperes): ")
            I_valor = float(entrada)
            break
        except ValueError:
            print("   Erro: Entrada inválida. Digite apenas números (ex: 10.5).")

    i_vetor = np.array([I_valor, -I_valor, 0.0, 0.0])
    print(f"\nVetor de correntes (i):\n{i_vetor}")
    print("-" * 50)
    input("\nPressione Enter para avançar")

    try:
        # Fatoração LU
        L, U = fatoracao_LU(G)
        y = substituicao_direta(L, i_vetor)
        v = substituicao_reversa(U, y)
        n = G.shape[0]

        print("\nSistema Original (G.v = i):\n")
        for i in range(n):
            linha = "  ".join([f"{G[i, j]:<6.1f}" for j in range(n)])
            print(f"| {linha} |   | v{i+1} |   | {i_vetor[i]:<6.2f} |")
        print("-" * 50)
        input("\nPressione Enter para avançar")

        print("\nDecomposição LU da matriz G:\n")
        print("Matriz L:\n", np.round(L, 4))
        print("\nMatriz U:\n", np.round(U, 4))
        print("-" * 50)
        input("\nPressione Enter para avançar")

        print("\nSolução do sistema:\n")
        for i in range(n):
            print(f"  v{i+1} = {v[i]:.4f} V")

        print("\n" + "=" * 50)
        input("\nPressione Enter para avançar")

    except (ValueError, ZeroDivisionError) as e:
        print(f"\nOcorreu um erro durante os cálculos: {e}")
        return

    # Análise para diferentes valores de I
    print("\n" + "=" * 100)
    print(" Análise da Tensão V34 (diferença de potencial entre v3 e v4) ")
    print("=" * 100)
    input("\nPressione Enter para iniciar a análise dos casos I = [5, 10, 15, 20, 25] A...")

    correntes_casos = [5.0, 10.0, 15.0, 20.0, 25.0]
    vetores_v = []
    tensoes_v34 = []

    # Fatora apenas uma vez
    L_auto, U_auto = fatoracao_LU(G)

    for I in correntes_casos:
        i_vetor = np.array([I, -I, 0.0, 0.0])
        y = substituicao_direta(L_auto, i_vetor)
        v = substituicao_reversa(U_auto, y)
        v34 = v[2] - v[3]

        vetores_v.append(v)
        tensoes_v34.append(v34)

    print("\nResultados para diferentes valores de I:\n")
    for idx, I in enumerate(correntes_casos):
        print(f"Para I = {I:.1f} A:")
        print(f"   v = {np.round(vetores_v[idx], 4)} V")
        print(f"   V34 = {tensoes_v34[idx]:.4f} V\n")

    input("Pressione Enter para mostrar o gráfico final...")

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(correntes_casos, tensoes_v34, marker='o', linestyle='-', color='blue')
    plt.title('Variação da Tensão V₃₄', fontsize=16)
    plt.xlabel('Corrente da Fonte I [A]', fontsize=12)
    plt.ylabel('Tensão V₃₄ [V]', fontsize=12)
    plt.xticks(correntes_casos)
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
