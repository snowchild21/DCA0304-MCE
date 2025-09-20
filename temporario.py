import numpy as np
import matplotlib.pyplot as plt

# --- Nossas Funções de Resolução (não mudam) ---

def fatoracao_LU(A):
    """Fatoração LU (Doolittle) sem pivoteamento."""
    A = np.array(A, dtype=float)
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError("Erro! A matriz deve ser quadrada.")
    L = np.zeros((n, n), dtype=float)
    U = np.zeros((n, n), dtype=float)
    for i in range(n):
        L[i, i] = 1.0
    for k in range(n):
        soma_u = sum(L[k, m] * U[m, k] for m in range(k))
        U[k, k] = A[k, k] - soma_u
        if abs(U[k, k]) < 1e-15:
            raise ZeroDivisionError(f"Pivô U[{k},{k}] é zero.")
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


# --- Bloco Principal com Fluxo Combinado ---
if __name__ == "__main__":
    
    G = np.array([
        [-4.0,  1.0,   2.0,   0.0],
        [ 1.0, -4.0,   0.0,   2.0],
        [ 2.0,  0.0, -24.0,  20.0],
        [ 0.0,  2.0,  20.0, -24.0]
    ])
    n = G.shape[0]

    # ==================================================================
    # PARTE 1: SOLUÇÃO INTERATIVA PARA UM CASO ESCOLHIDO PELO USUÁRIO
    # ==================================================================
    print("="*60)
    print("      PARTE 1: SOLUÇÃO INTERATIVA PASSO A PASSO")
    print("="*60)
    
    I_interativo = None
    while I_interativo is None:
        try:
            entrada = input(">> Digite um valor de corrente I para a análise detalhada: ")
            I_interativo = float(entrada)
        except ValueError:
            print("   Erro: Entrada inválida. Por favor, digite um número.")
            
    i_interativo = np.array([I_interativo, -I_interativo, 0.0, 0.0])
    
    # Resolvendo e mostrando cada passo
    L_int, U_int = fatoracao_LU(G)
    y_int = substituicao_direta(L_int, i_interativo)
    v_int = substituicao_reversa(U_int, y_int)
    
    print("\n--- Sistema Original (G.v = i) ---")
    for i in range(n):
        linha = "  ".join([f"{G[i, j]:<6.1f}" for j in range(n)])
        print(f"| {linha} | | v{i+1} | | {i_interativo[i]:<6.2f} |")
    input("\nPressione Enter para ver a Fatoração LU...")
    
    print("\n--- Matrizes L e U ---\n")
    print("Matriz L:\n", np.round(L_int, 4))
    print("\nMatriz U:\n", np.round(U_int, 4))
    input("\nPressione Enter para ver o sistema Ly = i...")

    print("\n--- Primeiro Sistema Triangular (L.y = i) ---\n")
    for i in range(n):
        linha = "  ".join([f"{L_int[i, j]:<6.1f}" for j in range(n)])
        print(f"| {linha} | | y{i+1} | | {i_interativo[i]:<6.2f} |")
    input("\nPressione Enter para ver o sistema Uv = y...")
    
    print("\n--- Segundo Sistema Triangular (U.v = y) ---\n")
    for i in range(n):
        linha = "  ".join([f"{U_int[i, j]:<7.2f}" for j in range(n)])
        print(f"| {linha} | | v{i+1} | | {y_int[i]:<7.2f} |")
    input("\nPressione Enter para ver a solução final deste caso...")
    
    print("\n--- Solução para I = {} A ---\n".format(I_interativo))
    for i, tensao in enumerate(v_int):
        print(f"  v{i+1} = {tensao:.4f} V")

    # ==================================================================
    # PARTE 2: ANÁLISE AUTOMÁTICA PARA CASOS FIXOS E GRÁFICO
    # ==================================================================
    print("\n\n" + "="*60)
    print("      PARTE 2: ANÁLISE AUTOMÁTICA PARA MÚLTIPLOS CASOS")
    print("="*60)
    input("\nPressione Enter para iniciar a análise dos casos I = [5, 10, 15, 20, 25] A...")

    correntes_casos = [5.0, 10.0, 15.0, 20.0, 25.0]
    vetores_v_solucao = []
    tensoes_v34 = []

    L_auto, U_auto = fatoracao_LU(G) # Fatora a matriz uma única vez

    for i_val in correntes_casos:
        i_vetor = np.array([i_val, -i_val, 0.0, 0.0])
        y = substituicao_direta(L_auto, i_vetor)
        v = substituicao_reversa(U_auto, y)
        v34 = v[2] - v[3]
        vetores_v_solucao.append(v)
        tensoes_v34.append(v34)
        
    print("\n--- Resumo dos Resultados Calculados ---\n")
    for i in range(len(correntes_casos)):
        print(f"--- Para I = {correntes_casos[i]:.1f} A ---")
        print(f"  Vetor v: {np.round(vetores_v_solucao[i], 4)} V")
        print(f"  Tensão V34: {tensoes_v34[i]:.4f} V\n")

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