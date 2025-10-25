import numpy as np
import matplotlib.pyplot as plt

# ==============================================================
# MÉTODO DE NEWTON-RAPHSON PARA SISTEMAS DE EQUAÇÕES NÃO LINEARES
# ==============================================================
# Sistema:
# f1(x,y) = x^2 + x*y - 10
# f2(x,y) = y + 3*x*y^2 - 57
# --------------------------------------------------------------


def F(X):
    """
    Calcula o vetor F(X) = [f1(x, y), f2(x, y)]^T
    Parâmetros:
        X: vetor numpy [x, y]
    Retorna:
        np.array([f1, f2])
    """
    x, y = X
    f1 = x**2 + x*y - 10
    f2 = y + 3*x*(y**2) - 57
    return np.array([f1, f2])


def J(X):
    """
    Calcula a matriz Jacobiana J(X):
        [df1/dx  df1/dy]
        [df2/dx  df2/dy]
    Parâmetros:
        X: vetor numpy [x, y]
    Retorna:
        np.array 2x2
    """
    x, y = X
    df1dx = 2*x + y
    df1dy = x
    df2dx = 3*(y**2)
    df2dy = 1 + 6*x*y
    return np.array([[df1dx, df1dy],
                     [df2dx, df2dy]])


# ==============================================================
# PARÂMETROS INICIAIS
# ==============================================================
X = np.array([10.0, 10.0])   # vetor inicial [x0, y0]
tol = 1e-5                   # tolerância
Nmax = 20                    # número máximo de iterações


def eliminacao_gauss(A, B):
    # Cópias para não alterar originais
    A = [row.copy() for row in A]
    B = [[b] if isinstance(b, (int, float)) else b.copy() for b in B]
    n = len(A)

    # Matriz aumentada
    for i in range(n):
        A[i].append(B[i][0])

    # Eliminação direta
    for i in range(n):
        piv = A[i][i]
        if abs(piv) < 1e-12:
            raise ValueError(f"Pivô zero detectado na linha {i}")
        for j in range(i, n+1):
            A[i][j] /= piv
        for k in range(i+1, n):
            fator = A[k][i]
            for j in range(i, n+1):
                A[k][j] -= fator * A[i][j]

    # Substituição regressiva
    Xsol = [0] * n
    for i in range(n-1, -1, -1):
        Xsol[i] = A[i][n]
        for j in range(i+1, n):
            Xsol[i] -= A[i][j] * Xsol[j]

    return np.array(Xsol)


# ==============================================================
# LOOP ITERATIVO DO MÉTODO DE NEWTON-RAPHSON
# ==============================================================
iteracoes = [X.copy()]  # armazena os vetores de cada iteração

print(f"| {'Iter':>4} | {'x':>12} | {'y':>12} | {'Δx':>13} | {'Δy':>13} |")
print("=" * 70)

for k in range(Nmax):
    Fx = F(X)
    Jx = J(X)

    delta = eliminacao_gauss(Jx.tolist(), (-Fx).tolist())

    X = X + delta
    iteracoes.append(X.copy())

    print(
        f"| {k+1:4d} | {X[0]:+12.6f} | {X[1]:+12.6f} | {delta[0]:+12.6e} | {delta[1]:+12.6e} |")

    if abs(delta[0]) < tol and abs(delta[1]) < tol:
        print(f"Convergência alcançada na iteração {k+1}")
        break
else:
    print("Número máximo de iterações atingido sem convergência.")

# ==============================================================
# RESULTADOS FINAIS
# ==============================================================
print("\nVetor solução (raízes encontradas):")
print(f"x = {X[0]:.6f}, y = {X[1]:.6f}")

# Calcula os valores das funções nas raízes
Fx_final = F(X)
print("\nValores das funções em (x, y):")
print(f"f1(x,y) = {Fx_final[0]:.6e}")
print(f"f2(x,y) = {Fx_final[1]:.6e}")

# ==============================================================
# PLOTAGEM DA EVOLUÇÃO DAS ITERAÇÕES
# ==============================================================
iteracoes = np.array(iteracoes)
plt.figure(figsize=(8, 5))
plt.plot(iteracoes[:, 0], iteracoes[:, 1], 'o-', label='Iterações (x,y)')
plt.title('Evolução das iterações – Método de Newton-Raphson')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()
