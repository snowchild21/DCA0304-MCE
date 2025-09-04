import numpy as np


def fatoracao_LU(A):
    """
    Fatoração LU ultilizando o metodo de Doolittle (O que ta nos slides de RP).
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError("XxXx Erro! A deve ser uma matriz quadrada. xXxX")

    L = np.zeros((n, n), dtype=float)
    U = np.zeros((n, n), dtype=float)

 
    for i in range(n):
        L[i, i] = 1.0

    for k in range(n):
        
        soma = sum(L[k, m] * U[m, k] for m in range(k))
        U[k, k] = A[k, k] - soma

        if abs(U[k, k]) < 1e-12:
            raise ZeroDivisionError(f"Erro: U[{k},{k}] = {U[k, k]} é muito próximo de zero.")

        
        for j in range(k + 1, n):
            soma = sum(L[k, m] * U[m, j] for m in range(k))
            U[k, j] = A[k, j] - soma

        
        for i in range(k + 1, n):
            soma = sum(L[i, m] * U[m, k] for m in range(k))
            L[i, k] = (A[i, k] - soma) / U[k, k]

    return L, U


if __name__ == "__main__":
    
    n = int(input("Digite a ordem da matriz quadrada A: "))
    A = []
    print("Digite a matriz A linha por linha (separando os elementos com espaço):")
    for i in range(n):
        linha = list(map(float, input(f"Linha {i+1}: ").split()))
        if len(linha) != n:
            raise ValueError("Número incorreto de elementos na linha.")
        A.append(linha)

    b = list(map(float, input("Digite o vetor b (separando os elementos com espaço): ").split()))
    if len(b) != n:
        raise ValueError("O vetor b deve ter o mesmo tamanho que A.")

    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Fatoração LU
    L, U = fatoracao_LU(A)

    print("\nMatriz A:")
    print(A)
    print("\nMatriz L:")
    print(L)
    print("\nMatriz U:")
    print(U)

    # Obs: aqui apenas fatoração. Para resolver Ax=b,
    # reutilize métodos de substituição direta e reversa já implementados.
