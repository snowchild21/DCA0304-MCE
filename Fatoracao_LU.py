import numpy as np

def fatoracao_LU(A):
    """
    Este metodo consiste em quebrarmos o sistema Gv = i em dois sistemas triangulares:
    onde G = LU (fatoração LU)
    (LU)v = i
    Ly = i  (substituição direta, pois L é triangular inferior)
    Uv = y  (substituição reversa pois U é triangular superior)
    
    Ao resolvermos esses dois sistemas, obtemos o vetor v.
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError("Erro Critico. A matriz deve ser quadrada.")

    L = np.zeros((n, n), dtype=float)
    U = np.zeros((n, n), dtype=float)

    for i in range(n):
        L[i, i] = 1.0

    for k in range(n):
        soma_u = sum(L[k, m] * U[m, k] for m in range(k))
        U[k, k] = A[k, k] - soma_u

        
        if abs(U[k, k]) < 1e-15:
            raise ZeroDivisionError(f"Erro critico. Pivô U[{k},{k}] é zero. Fatoração LU falhou.")

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
    """Resolve o sistema Ux = y (ou Gv = y no nosso caso)."""
    n = U.shape[0]
    v = np.zeros(n, dtype=float)

    for i in range(n - 1, -1, -1):
        soma = sum(U[i, j] * v[j] for j in range(i + 1, n))
        v[i] = (y[i] - soma) / U[i, i]
        
    return v


# hora de resolver o sistema do circuito.


if __name__ == "__main__":
    
    # Matriz de condutâncias G 
    G = np.array([
        [-4.0,  1.0,   2.0,   0.0],
        [ 1.0, -4.0,   0.0,   2.0],
        [ 2.0,  0.0, -24.0,  20.0],
        [ 0.0,  2.0,  20.0, -24.0]
    ])
    

    
    print("="*100)
    print("   TECNICA DA ANALISE NODAL - Resolucao por Fatoracao LU")
    print("="*100)
    
    
    print("\n Matriz de Condutâncias (G) do circuito [mho]:\n")
    print(G)
    print("-"*50)

    input("\nPressione Enter para avançar")

    print("\nFonte de Corrente I:")
    
    I_valor = None
    while I_valor is None:
        try:
            # Pede a entrada e tenta converter para float
            entrada = input(">> Por favor, digite o valor para a corrente I (em Amperes): ")
            I_valor = float(entrada)
        except ValueError:
            # Se a conversão falhar, informa o erro e continua o loop
            print("   Erro: Entrada inválida. Por favor, digite um número (ex: 10.5).")
            
    
    i_vetor = np.array([I_valor, -I_valor, 0.0, 0.0])
    print(f"\n   O vetor de fontes de corrente 'i' foi definido como:\n{i_vetor}")
    print("-"*50)
    input("\nPressione Enter para avançar")

    try:
        
        L, U = fatoracao_LU(G)
        y = substituicao_direta(L, i_vetor)
        v = substituicao_reversa(U, y)
        n = G.shape[0]

        
        print("\n Sistema Original a ser Resolvido (G.v = i):\n")
        for i in range(n):
            linha = "  ".join([f"{G[i, j]:<6.1f}" for j in range(n)])
            print(f"| {linha} |   | v{i+1} |   | {i_vetor[i]:<6.2f} |")
        print("-"*50)
        input("\nPressione Enter para avançar")

        
        print("\n) Após a Fatoração (L.U.v = i):\n")
        print("Onde a matriz G foi decomposta em L e U:")
        print("\nMatriz L:\n", np.round(L, 4))
        print("\nMatriz U:\n", np.round(U, 4))
        print("-"*50)
        input("\nPressione Enter para avançar")

        
        print("\n (L.y = i) resolvido por Substituicao Direta :\n")
        for i in range(n):
            linha = "  ".join([f"{L[i, j]:<6.1f}" for j in range(n)])
            print(f"| {linha} |   | y{i+1} |   | {i_vetor[i]:<6.2f} |")
        print("-"*50)
        input("\nPressione Enter para avançar")

        
        print("\n (U.v = y) resolvido por Substituicao Reversa:\n")
        for i in range(n):
            linha = "  ".join([f"{U[i, j]:<7.2f}" for j in range(n)])
            print(f"| {linha} |   | v{i+1} |   | {y[i]:<7.2f} |")
        print("-"*50)
        input("\nPressione Enter para avançar")

        
        print("\n Solução: Vetor das Tensões Nodais:\n")
        
        for i in range(n):
            print(f"  v{i+1} = {v[i]:.4f} V")
            
        print("\n" + "="*50)
        input("\nPressione Enter para avançar")


        print("\n" + "="*60)
        print("   COMPARAÇÃO COM A SOLUÇÃO DIRETA DO NUMPY")
        print("="*60)
        
        
        v_numpy = np.linalg.solve(G, i_vetor)
        
        print("\nResultado usando np.linalg.solve(G, i):\n")
        for i in range(n):
            print(f"  v{i+1} = {v_numpy[i]:.8f} V")
        
        print("\n--- Módulo da Diferença Para Cada Tensão Nodal ---\n")
        for i in range(n):
            diferenca = np.abs(v[i] - v_numpy[i])
            
            print(f"  Diferença em v{i+1}: |v - v_numpy| = {diferenca:.2e}")

        
    except (ValueError, ZeroDivisionError) as e:
        print(f"\nOcorreu um erro durante os cálculos: {e}")