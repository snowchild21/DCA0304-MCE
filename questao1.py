import numpy as np
import matplotlib.pyplot as plt

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
            
    except (ValueError, ZeroDivisionError) as e:
        print(f"\nOcorreu um erro durante os cálculos: {e}")
    print("\n\n" + "="*100)
    print("      Analise da Tensão V34 (tensao entre a condutancia G_6) para Diferentes Valores de I")
    print("="*100)
    input("\nPressione Enter para iniciar a análise dos casos I = [5, 10, 15, 20, 25] A...")

    correntes_casos = [5.0, 10.0, 15.0, 20.0, 25.0]
    vetores_v = []
    tensoes_v34 = []

    L_auto, U_auto = fatoracao_LU(G) # Fatora a matriz uma única vez

    for i_casos in correntes_casos:
        i_vetor = np.array([i_casos, -i_casos, 0.0, 0.0])
        y = substituicao_direta(L_auto, i_vetor)
        v = substituicao_reversa(U_auto, y)
        v34 = v[2] - v[3]
        vetores_v.append(v)
        tensoes_v34.append(v34)
        
    print("\n\n")
    for i in range(len(correntes_casos)):
        print(f"Para I = {correntes_casos[i]:.1f} A ")
        print(f"Vetor v: {np.round(vetores_v[i], 4)} V")
        print(f"Tensão V34: {tensoes_v34[i]:.4f} V\n")

    input("Pressione Enter para mostrar o gráfico final...")

    # Plotagem do gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(correntes_casos, tensoes_v34, marker='o', linestyle='--', color='r')
    plt.title('Variação da Tensão V₃₄ em Função da Corrente da Fonte I', fontsize=16)
    plt.xlabel('Corrente da Fonte, I [A]', fontsize=12)
    plt.ylabel('Tensão V₃₄ = (V₃ - V₄) [V]', fontsize=12)
    plt.xticks(correntes_casos)
    plt.grid(True)
    plt.show()