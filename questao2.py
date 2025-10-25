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

# ==============================================================
# LOOP ITERATIVO DO MÉTODO DE NEWTON-RAPHSON
# ==============================================================
iteracoes = [X.copy()]  # armazena os vetores de cada iteração

for k in range(Nmax):
    # Calcula F(X) e J(X)
    Fx = F(X)
    Jx = J(X)

    # Calcula a variação ΔX = -J^{-1}(X) * F(X)
    delta = np.linalg.solve(Jx, -Fx)

    # Atualiza o vetor X
    X = X + delta
    iteracoes.append(X.copy())

    # Critério de parada: norma infinita da variação menor que tolerância
    if np.linalg.norm(delta, ord=np.inf) < tol:
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
plt.figure(figsize=(8,5))
plt.plot(iteracoes[:,0], iteracoes[:,1], 'o-', label='Iterações (x,y)')
plt.title('Evolução das iterações – Método de Newton-Raphson')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()
